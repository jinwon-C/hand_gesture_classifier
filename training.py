import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import numpy as np
import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
import loadcsvData as ld
import openmax_module as opmodule
#Data 폴더
DirName = "/home/cjw/data/wintest/win5000/"
#Kind = ["raw","left-right","updown","circle","block","right-left","downup","triangle"]
Kind = ["nothing","left-right","up-down","circle","block","right-left"]
#xData, yData = ld.load_data_jh(DirName, Kind)
xTrain, yTrain, xTest, yTest = ld.load_data(DirName,Kind,0.8)

#KFOLD = 5

sess = tf.InteractiveSession()
x = tf.placeholder(tf.float32, [None, 344,20])
y_= tf.placeholder(tf.float32, [None, 6])
W = tf.Variable(tf.zeros([344,20,6]))
b = tf.Variable(tf.zeros([6]))
y = tf.nn.softmax(tf.matmul(x, W) + b)

# 원하는 행렬 사이즈로 초기 값을 만들어서 리턴하는 메서드
def weight_variable(shape):
	initial = tf.truncated_normal(shape, stddev=0.1)
	return tf.Variable(initial)
# 0.1 로 초기값 지정하여 원하는 사이즈로 리턴
def bias_variable(shape):
	initial = tf.constant(0.1, shape=shape)
	return tf.Variable(initial)

def conv2d(x, W):
	return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')

def max_pool_7x7(x):
	return tf.nn.max_pool(x, ksize=[1, 1, 7, 1],strides=[1, 1, 7, 1], padding='SAME')

def max_pool_5x5(x):
	return tf.nn.max_pool(x, ksize=[1, 1, 5, 1],strides=[1, 1, 5, 1], padding='SAME')

def max_pool_1x2(x):
	return tf.nn.max_pool(x, ksize=[1, 1, 2, 1],strides=[1, 1, 2, 1], padding='SAME')

def max_pool_1x4(x):
	return tf.nn.max_pool(x, ksize=[1, 1, 4, 1],strides=[1, 1, 4, 1], padding='SAME')

def max_pool_2x2(x):
	#return tf.nn.max_pool(x,ksize=[1,2,2,1],strides=[1,2,2,1], padding='SAME')
	return tf.nn.max_pool(x, ksize=[1, 2, 2, 1],strides=[1, 2, 2, 1], padding='SAME')

def aver_pool_3x3(x):
	#return tf.nn.max_pool(x,ksize=[1,2,2,1],strides=[1,2,2,1], padding='SAME')
	return tf.nn.avg_pool(x, ksize=[1, 3, 2, 1],strides=[1, 3, 2, 1], padding='SAME')

with tf.device('/gpu:1'):
	#커널 size = weight 갯수, 입력 갯수, 출력 갯수
	W_conv1 = weight_variable([1, 3, 1, 4])
	#bias = 출력 갯수= kernel 수= filter 수
	b_conv1 = bias_variable([4])
	x_image = tf.reshape(x, [-1,20,344,1])
	h_conv1 = tf.nn.relu(conv2d(x_image, W_conv1) + b_conv1)
	h_pool1 = max_pool_5x5(h_conv1)
									
	W_conv2 = weight_variable([1, 3, 4, 8])
	b_conv2 = bias_variable([8])
	h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2)
	h_pool2 = max_pool_1x4(h_conv2)

#h2 = tf.nn.dropout(h_pool2,0.5)

	W_conv3 = weight_variable([1, 3, 8, 16])
	b_conv3 = bias_variable([16])
	h_conv3 = tf.nn.relu(conv2d(h_pool2, W_conv3) + b_conv3)
	h_pool3 = max_pool_1x2(h_conv3)

	W_conv4 = weight_variable([1, 3, 16, 32])
	b_conv4 = bias_variable([32])
	h_conv4 = tf.nn.relu(conv2d(h_pool3, W_conv4) + b_conv4)
	h_pool4 = max_pool_1x2(h_conv4)

	W_conv5 = weight_variable([1, 3, 32, 64])
	b_conv5 = bias_variable([64])
	h_conv5 = tf.nn.relu(conv2d(h_pool4, W_conv5) + b_conv5)
	h_pool5 = max_pool_1x2(h_conv5)

#h5 = tf.nn.dropout(h_pool5,0.5)
	
	W_conv6 = weight_variable([1, 3, 64, 128])
	b_conv6 = bias_variable([128])
	h_conv6 = tf.nn.relu(conv2d(h_pool5, W_conv6) + b_conv6)
	h_pool6 = max_pool_2x2(h_conv6)
	
	
	W_conv7 = weight_variable([1, 3, 128, 256])
	b_conv7 = bias_variable([256])
	h_conv7 = tf.nn.relu(conv2d(h_pool6, W_conv7) + b_conv7)
	h_pool7 = max_pool_2x2(h_conv7)

	W_conv8 = weight_variable([1, 3, 256, 512])
	b_conv8 = bias_variable([512])
	h_conv8 = tf.nn.relu(conv2d(h_pool7, W_conv8) + b_conv8)
	h_pool8 = max_pool_2x2(h_conv8)


	h_pool_aver = aver_pool_3x3(h_pool8)
	h_pool2_flat = tf.reshape(h_pool_aver, [-1, 1* 1 * 512])

# drop out 연산의 결과를 담을 변수
	keep_prob = tf.placeholder(tf.float32)
	#h_fc1_drop2 = tf.nn.dropout(h_pool2_flat, keep_prob)
									
	W_fc3 = weight_variable([512, 6])
	b_fc3 = bias_variable([6])
	activation_vector=tf.matmul(h_pool2_flat, W_fc3) + b_fc3
	y_conv=tf.nn.softmax(activation_vector)
									
# Define loss and optimizer
	cross_entropy = -tf.reduce_sum(y_*tf.log(tf.clip_by_value(y_conv,1e-10,1.0)))
	train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)
	correct_prediction = tf.equal(tf.argmax(y_conv,1), tf.argmax(y_,1))
	accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
									
saver = tf.train.Saver()
sess.run(tf.initialize_all_variables())
for i in range(16000):
	batch_X,batch_Y = ld.next_batchTraining(Kind)
	batch_X = np.asarray(batch_X)
	batch_Y = np.asarray(batch_Y)
	batch_X = batch_X.reshape(60,344,20)
	batch_Y = ld.OneAndHot(batch_Y,Kind)
	if i%100 ==0:
		train_accuracy = accuracy.eval(feed_dict={x:batch_X, y_: batch_Y, keep_prob: 1.0})
		print("step %d, training accuracy %g"%(i, train_accuracy))
		
	train_step.run(feed_dict={x: batch_X, y_: batch_Y, keep_prob: 0.5})

xTrain = np.asarray(xTrain)
xTrain = xTrain.reshape(480,344,20)
yTrain = np.asarray(yTrain)
yTrain = ld.OneAndHot(yTrain, Kind)
av,y_conv_data = sess.run([activation_vector,y_conv],feed_dict={x:xTrain,y_:yTrain,keep_prob:1.0})
opmodule.create_training_data(av,y_conv_data,yTrain,Kind)

save_path = saver.save(sess,"model.ckpt")

xTest = np.asarray(xTest)
xTest = xTest.reshape(120,344,20)
yTest = np.asarray(yTest)
yTest = ld.OneAndHot(yTest, Kind)

print("test accuracy %g"%accuracy.eval(feed_dict={x:xTest, y_: yTest, keep_prob: 1.0}))

y = sess.run(y_conv, feed_dict={x:xTest,keep_prob:1.0})

sess.close()
