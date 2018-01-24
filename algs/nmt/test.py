
import utils, model

params = [(u'attention', u''), (u'attention_architecture', u'standard'), \
          (u'avg_ckpts', False), (u'batch_size', 128), (u'beam_width', 0),\
          (u'best_bleu', 0), (u'best_bleu_dir', u'/tmp/nmt_model/best_bleu'),\
          (u'check_special_token', True), (u'colocate_gradients_with_ops', True),\
          (u'decay_scheme', u''), (u'dev_prefix', u'/home/burak/Downloads/tur-eng/tst2012'),\
          (u'dropout', 0.2), (u'embed_prefix', None), (u'encoder_type', u'uni'), \
          (u'eos', u'</s>'), (u'epoch_step', 0), (u'forget_bias', 1.0),\
          (u'infer_batch_size', 32), (u'init_op', u'uniform'), \
          (u'init_weight', 0.1), (u'learning_rate', 1.0), \
          (u'length_penalty_weight', 0.0), (u'log_device_placement', False), \
          (u'max_gradient_norm', 5.0), (u'max_train', 0), (u'metrics', [u'bleu']), \
          (u'num_buckets', 5), (u'num_decoder_layers', 2), (u'num_decoder_residual_layers', 0),\
          (u'num_embeddings_partitions', 0), (u'num_encoder_layers', 2),\
          (u'num_encoder_residual_layers', 0), (u'num_gpus', 1), \
          (u'num_inter_threads', 0), (u'num_intra_threads', 0), \
          (u'num_keep_ckpts', 5), (u'num_layers', 2), (u'num_train_steps', 12000), \
          (u'num_translations_per_input', 1), (u'num_units', 128), \
          (u'optimizer', u'sgd'), (u'out_dir', u'/tmp/nmt_model'), \
          (u'output_attention', True), (u'override_loaded_hparams', False), \
          (u'pass_hidden_state', True), (u'random_seed', None), \
          (u'residual', False), (u'sampling_temperature', 0.0), \
          (u'share_vocab', False), (u'sos', u'<s>'), (u'src', u'en'), \
          (u'src_embed_file', u''), (u'src_max_len', 50), \
          (u'src_max_len_infer', None), (u'src_vocab_file', u'/tmp/nmt_model/vocab.en'), \
          (u'src_vocab_size', 24646), (u'steps_per_external_eval', None), \
          (u'steps_per_stats', 100), (u'subword_option', u''), \
          (u'test_prefix', u'/home/burak/Downloads/tur-eng/tst2013'), \
          (u'tgt', u'tr'), (u'tgt_embed_file', u''), (u'tgt_max_len', 50), \
          (u'tgt_max_len_infer', None), (u'tgt_vocab_file', u'/tmp/nmt_model/vocab.tr'), \
          (u'tgt_vocab_size', 106604), (u'time_major', True), \
          (u'train_prefix', u'/home/burak/Downloads/tur-eng/train'), \
          (u'unit_type', u'lstm'), (u'vocab_prefix', u'/home/burak/Downloads/tur-eng/vocab'), \
          (u'warmup_scheme', u't2t'), (u'warmup_steps', 0)]
	  
hparams = dict((k,v) for (k,v) in params)
  
model_creator = model.Model
infer_model = utils.create_infer_model(model_creator, hparams)

import tensorflow as tf
import inference, os, time

log_device_placement = hparams['log_device_placement']
out_dir = hparams['out_dir']
num_train_steps = hparams['num_train_steps']
steps_per_stats = hparams['steps_per_stats']
steps_per_external_eval = hparams['steps_per_external_eval']
steps_per_eval = 10 * steps_per_stats
avg_ckpts = hparams['avg_ckpts']
dev_src_file = "%s.%s" % (hparams['dev_prefix'], hparams['src'])
dev_tgt_file = "%s.%s" % (hparams['dev_prefix'], hparams['tgt'])
print (dev_src_file)
print (dev_tgt_file)
sample_src_data = inference.load_data(dev_src_file)
sample_tgt_data = inference.load_data(dev_tgt_file)

summary_name = "train_log"
model_dir = hparams['out_dir']

# Log and output files
log_file = os.path.join(out_dir, "log_%d" % time.time())
log_f = tf.gfile.GFile(log_file, mode="a")
utils.print_out("# log_file=%s" % log_file, log_f)

config_proto = utils.get_config_proto(
    log_device_placement=log_device_placement,
    num_intra_threads=hparams['num_intra_threads'],
    num_inter_threads=hparams['num_inter_threads'])

infer_sess = tf.Session(target='', config=config_proto, graph=infer_model.graph)

import train, inference

model_dir = "/home/burak/Downloads/nmt_model1/translate.ckpt-9000"
with infer_model.graph.as_default():
    loaded_infer_model, global_step = utils.load_model(
#    loaded_infer_model, global_step = utils.create_or_load_model(
        infer_model.model, model_dir, infer_sess, "infer")

sample_src_data = inference.load_data(dev_src_file)
sample_tgt_data = inference.load_data(dev_tgt_file)

summary_writer = tf.summary.FileWriter("/tmp/out", infer_model.graph)

train._sample_decode(loaded_infer_model, global_step, infer_sess, hparams,
                     infer_model.iterator, sample_src_data, sample_tgt_data,
                     infer_model.src_placeholder,
                     infer_model.batch_size_placeholder, summary_writer)











