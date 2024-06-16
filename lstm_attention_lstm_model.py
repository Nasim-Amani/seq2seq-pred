# -*- coding: utf-8 -*-
"""lstm_attention_lstm_model.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1AoGO_xWXy5_31v8Au1kzRwLLyU9QVOOz
"""



def lstm_attention_lstm_model(num_layers, units, learning_rate, decoder_dropout_rates, encoder_dropout_rates,use_batch_norm):
    # Create the encoder input layer
    encoder_inputs = tf.keras.layers.Input(shape=(X_train.shape[1], X_train.shape[2]))

    # Encoding layer
    encoder_outputs_and_states = encoder_inputs
    encoder_states = []
    for i in range(num_layers):
        # Create the encoder LSTM layer
        encoder_lstm = LSTM(units=units[i], return_sequences=True, return_state=True, name=f'encoder_lstm_{i+1}')
        encoder_outputs_and_states = encoder_lstm(encoder_outputs_and_states)
        encoder_states.extend(encoder_outputs_and_states[1:])
        encoder_outputs_and_states = encoder_outputs_and_states[0]
        # Apply dropout to the encoder layer
        enc_dropout = Dropout(rate=encoder_dropout_rates[i])(encoder_outputs_and_states)

        # Apply batch normalization if specified
        if use_batch_norm:
          encoder_bn = BatchNormalization()(enc_dropout)
        else:
          encoder_bn = enc_dropout

        encoder_outputs_and_states = encoder_bn  # Connect the dropout layer to the next layer

    # Attention layer
    attention_layer = keras.layers.Attention()
    out_attention = attention_layer([encoder_bn, encoder_bn, encoder_bn])

    # Decoder
    decoder_outputs = out_attention

    for i in range(num_layers):
        # Create the decoder LSTM layer
        decoder_lstm = LSTM(units=units[i], return_sequences=True if i < num_layers - 1 else False,
                           return_state=True, name=f'decoder_lstm_{i+1}')
        decoder_outputs_and_states = decoder_lstm(out_attention, initial_state=encoder_states[2*i:2*(i+1)])
        decoder_outputs = decoder_outputs_and_states[0]
        # Apply dropout to the decoder layer
        decoder_dropout = Dropout(rate=decoder_dropout_rates[i])(decoder_outputs)

        # Apply batch normalization if specified
        if use_batch_norm:
            decoder_bn = BatchNormalization()(decoder_dropout)
        else:
            decoder_bn = decoder_dropout

        decoder_outputs = decoder_bn  # Connect the dropout layer to the next layer

    # Create the output dense layer
    decoder_dense = keras.layers.Dense(1, activation='linear')
    decoder_outputs = decoder_dense(decoder_outputs)

    # Create the model
    model = Model(encoder_inputs, decoder_outputs)
    optimizer = keras.optimizers.Adam(learning_rate=learning_rate)
    model.compile(optimizer=optimizer, loss='mean_squared_error')
    return model

units=[64]
num_layers=1
encoder_dropout_rates=[0.1]
decoder_dropout_rates=[0.4]
learning_rate=0.001
use_batch_norm=False
batch_size=32
model = lstm_attention_lstm_model(units=units, num_layers=num_layers, encoder_dropout_rates=encoder_dropout_rates,
                    decoder_dropout_rates=decoder_dropout_rates, learning_rate=learning_rate , use_batch_norm=use_batch_norm
                   )
model.summary()