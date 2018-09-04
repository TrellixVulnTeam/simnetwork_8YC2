import tensorflow as tf
import numpy as np

from tensor2tensor.models.research import universal_transformer, universal_transformer_util
from tensor2tensor.models import transformer


def universal_transformer_encoder(inputs, target_space, 
				hparams, features=None, make_image_summary=False):
    
    encoder_input, self_attention_bias, encoder_decoder_attention_bias = (
        transformer.transformer_prepare_encoder(
            inputs, target_space, hparams, features=features))

    encoder_input = tf.nn.dropout(encoder_input,
                                  1.0 - hparams.layer_prepostprocess_dropout)

    [encoder_output, 
    encoder_extra_output] = universal_transformer_util.universal_transformer_encoder(
        encoder_input,
        self_attention_bias,
        hparams,
        nonpadding=transformer.features_to_nonpadding(features, "inputs"),
        save_weights_to=None,
        make_image_summary=make_image_summary)

    # encoder_output = tf.expand_dims(encoder_output, 2)

    return encoder_output
