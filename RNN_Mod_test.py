#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar  3 16:12:02 2019

@author: yuedai
"""

import tensorflow as tf
tf.enable_eager_execution()

import numpy as np
import os
import sys
#import time


def split_input_target(chunk):
    input_text = chunk[:-1]
    target_text = chunk[1:]
    return input_text, target_text

# Using sparse_softmax_cross_entropy so that we don't have to create one-hot vectors
def loss_function(real, preds):
    return tf.losses.sparse_softmax_cross_entropy(labels=real, logits=preds)


class Model(tf.keras.Model):
  def __init__(self, vocab_size, embedding_dim, units):
    super(Model, self).__init__()
    self.units = units

    self.embedding = tf.keras.layers.Embedding(vocab_size, embedding_dim)

    if tf.test.is_gpu_available():
      self.gru1 = tf.keras.layers.CuDNNGRU(self.units,
                                          return_sequences=True,
                                          recurrent_initializer='glorot_uniform',
                                          stateful=True)
    else:
      self.gru1 = tf.keras.layers.GRU(self.units,
                                     return_sequences=True,
                                     recurrent_activation='sigmoid',
                                     recurrent_initializer='glorot_uniform',
                                     stateful=True)
      
    if tf.test.is_gpu_available():
      self.gru2 = tf.keras.layers.CuDNNGRU(self.units,
                                          return_sequences=True,
                                          recurrent_initializer='glorot_uniform',
                                          stateful=True)
    else:
      self.gru2 = tf.keras.layers.GRU(self.units,
                                     return_sequences=True,
                                     recurrent_activation='sigmoid',
                                     recurrent_initializer='glorot_uniform',
                                     stateful=True)

    self.fc = tf.keras.layers.Dense(vocab_size)

  def call(self, x):
    embedding = self.embedding(x)

    # output at every time step
    # output shape == (batch_size, seq_length, hidden_size)
    output1 = self.gru1(embedding)
    
    # output at every time step
    # output shape == (batch_size, seq_length, hidden_size)
    output2 = self.gru2(output1)

    # The dense layer will output predictions for every time_steps(seq_length)
    # output shape after the dense layer == (seq_length * batch_size, vocab_size)
    prediction = self.fc(output2)

    # states will be used to pass at every step to the model while training
    return prediction

if __name__=="__main__":

#    path_to_file = sys.argv[1]
    path_to_file = './english/train'
    
    text = open(path_to_file).read()
    ## length of text is the number of characters in it
    #print ('Length of text: {} characters'.format(len(text)))
    ## Take a look at the first 1000 characters in text
    #print(text[:1000])
    
    # The unique characters in the file
    vocab = sorted(set(text))
    #print ('{} unique characters'.format(len(vocab)))
    
    # Creating a mapping from unique characters to indices
    char2idx = {u:i for i, u in enumerate(vocab)}
    idx2char = np.array(vocab)
    
    text_as_int = np.array([char2idx[c] for c in text])
    
    #for char,_ in zip(char2idx, range(20)):
    #    print('{:6s} ---> {:4d}'.format(repr(char), char2idx[char]))
    ## Show how the first 13 characters from the text are mapped to integers
    #print ('{} ---- characters mapped to int ---- > {}'.format(text[:13], text_as_int[:13]))
    
    # The maximum length sentence we want for a single input in characters
    seq_length = 50
    
    # Create training examples / targets
    chunks = tf.data.Dataset.from_tensor_slices(text_as_int).batch(seq_length+1, drop_remainder=True)
    
    #for item in chunks.take(5):
    #  print(repr(''.join(idx2char[item.numpy()])))
    
    dataset = chunks.map(split_input_target)
    #for input_example, target_example in  dataset.take(1):
    #  print ('Input data: ', repr(''.join(idx2char[input_example.numpy()])))
    #  print ('Target data:', repr(''.join(idx2char[target_example.numpy()])))
    
    # Batch size
    BATCH_SIZE = 64
    
    # Buffer size to shuffle the dataset
    BUFFER_SIZE = 10000
    
    dataset = dataset.shuffle(BUFFER_SIZE).batch(BATCH_SIZE, drop_remainder=True)
    
    # Length of the vocabulary in chars
    vocab_size = len(vocab)
    
    # The embedding dimension
    embedding_dim = 128
    
    # Number of RNN units
    units = 256
    
    model = Model(vocab_size, embedding_dim, units)
    
    # Using adam optimizer with default arguments
    optimizer = tf.train.AdamOptimizer()
    
    #build model
    model.build(tf.TensorShape([BATCH_SIZE, seq_length]))
    model.summary()
    
    #save checkpoint
    # Directory where the checkpoints will be saved
    checkpoint_dir = './training_checkpoints_mod'
    # Name of the checkpoint files
    checkpoint_prefix = os.path.join(checkpoint_dir, "ckpt")
    
#    #Train epochs
#    EPOCHS = 5
#    # Training loop
#    for epoch in range(EPOCHS):
#        start = time.time()
#    
#        # initializing the hidden state at the start of every epoch
#        # initally hidden is None
#        hidden = model.reset_states()
#    
#        for (batch, (inp, target)) in enumerate(dataset):
#              with tf.GradientTape() as tape:
#                  # feeding the hidden state back into the model
#                  # This is the interesting step
#                  predictions = model(inp)
#                  loss = loss_function(target, predictions)
#    
#              grads = tape.gradient(loss, model.variables)
#              optimizer.apply_gradients(zip(grads, model.variables))
#    
#              if batch % 100 == 0:
#                  print ('Epoch {} Batch {} Loss {:.4f}'.format(epoch+1,
#                                                                batch,
#                                                                loss))
#        # saving (checkpoint) the model every 5 epochs
#        if (epoch + 1) % 5 == 0:
#          model.save_weights(checkpoint_prefix)
#    
#        print ('Epoch {} Loss {:.4f}'.format(epoch+1, loss))
#        print ('Time taken for 1 epoch {} sec\n'.format(time.time() - start))
#        
#    model.save_weights(checkpoint_prefix)
    
    
    model = Model(vocab_size, embedding_dim, units)

    model.load_weights(tf.train.latest_checkpoint(checkpoint_dir))
    
    model.build(tf.TensorShape([1, None]))
    
    # Evaluation step (generating text using the learned model)
#    test_file_path = sys.argv[2]
    test_file_path = './english/test'
#    total = 0
    hit = 0
    
    test_file = open(test_file_path).read()
    # Number of characters to generate
    num_generate = len(test_file) - 1
    
    # You can change the start string to experiment
    start_string = test_file[0]
    
    # Converting our start string to numbers (vectorizing)
    input_eval = [char2idx[s] for s in start_string]
    input_eval = tf.expand_dims(input_eval, 0)
    
    # Empty string to store our results
    text_generated = []
    
    # Low temperatures results in more predictable text.
    # Higher temperatures results in more surprising text.
    # Experiment to find the best setting.
    temperature = 1.0
    
    # Evaluation loop.
    total = len(test_file)
    hit = 0

    # Here batch size == 1
    model.reset_states()
    for i in range(num_generate):
        predictions = model(input_eval)
        # remove the batch dimension
        predictions = tf.squeeze(predictions, 0)
    
        # using a multinomial distribution to predict the word returned by the model
        predictions = predictions / temperature
        predicted_id = tf.multinomial(predictions, num_samples=1)[-1,0].numpy()
        
        if idx2char[predicted_id] == test_file[i + 1]:
            hit += 1
    
        # We pass the correct word as the next input to the model
        # along with the previous hidden state
        nextchar = test_file[i + 1]
        input_eval = [char2idx[s] for s in nextchar]
        input_eval = tf.expand_dims(input_eval, 0)
    
        text_generated.append(idx2char[predicted_id])
        
#    total = len(test_file)
#    res = start_string + ''.join(text_generated)
#    hit = 0
#    for i in range(len(test_file)):
#        total += 1
#        if test_file[i] == res[i]: hit += 1
#        
    finalAccu = hit/total
    print("The RNN accuracy is: " + str(finalAccu))