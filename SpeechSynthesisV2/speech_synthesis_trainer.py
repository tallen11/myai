import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='3'
from speech_synthesis_data_batcher import SpeechSynthesisDataBatcher
from speech_synthesis_model import SpeechSynthesisModel
import tensorflow as tf

train_data_path = os.path.join("data", "generated", "development_samples")
test_data_path = os.path.join("data", "generated", "test_samples")
phone_map_path = os.path.join("data", "generated", "phone_map.txt")

batcher = SpeechSynthesisDataBatcher(train_data_path, test_data_path)
print("Building model...")
model = SpeechSynthesisModel(input_sequence_length=256, vocab_size=batcher.get_vocab_size(phone_map_path), output_sequence_length=512, output_size=512)
saver = tf.train.Saver()

epochs = 400
batch_size = 30

print("Beginning training...")
with tf.Session() as session:
    session.run(tf.global_variables_initializer())
    current_epoch = 0
    current_step = 0
    while current_epoch < epochs:
        phones_batch, spect_batch, epoch_complete = batcher.get_batch(batch_size)
        print(spect_batch.shape)
        model.train_model(session, inputs=phones_batch, labels=spect_batch)
        if epoch_complete:
            if (current_epoch+1) % 4 == 0:
                avg_acc = 0.0
                # count = 0
                # for phones_test_batch, spect_test_batch in batcher.get_test_batches():
                #     avg_acc += model.get_loss(session, inputs=phones_test_batch, labels=spect_test_batch)
                #     count += 1
                # avg_acc /= count
                # saver.save(session, os.path.join("checkpoints", "speech_synthesis_model"))
                print("Epoch {} | loss: {}".format(current_epoch+1, avg_acc))
            current_epoch += 1
