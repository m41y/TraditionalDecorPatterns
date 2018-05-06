The objective was to classify images from https://www.kaggle.com/olgabelitskaya/traditional-decor-patterns/data, with restriction that only products must be classified. All this using TensorFlow For Poets tutorials script, retrain.py. Possible classifications are by country, by decor and by type. But as mentioned earlier type was set to product by restriction in given task. That leave us with 2 classifications, by country and by décor, with is done by doing below steps:

1.download (“Download All”) and unzip dataset from  https://www.kaggle.com/olgabelitskaya/traditional-decor-patterns/data, creating directory named like: foo/bar/traditional-decor-patterns;

2. in created directory (foo/bar/traditional-decor-patterns) unzip file decor.zip, creating directory foo/bar/traditional-decor-patterns/decor filed with images;

3.download TensorFlow For Poets by opening terminal and typing:
	git clone https://github.com/googlecodelabs/tensorflow-for-poets-2

4.from this repository copy file data_manipulation.py (or  processing.ipynb if you want to see more data insights) and open it in text editor, you must change the line 10 decor_path=” ” to decor_path = “<foo/bar/traditional-decor-patterns>”, save changes and run script by typing in terminal:
	python3 data_manipulation.py
this will create and populate with images 3 directories ‘jpegs’ ,containing .jpg version of datasets .png images, ‘country’ and ‘decor’ with are used by retrain.py script from  TensorFlow For Poets repository as a category labels;

5.change directory in terminal to tensorflow-for-poets-2 (type <cd  tensorflow-for-poets-2>) and run one of the below experiments by copy-pasting run parameters (paragraphs that starts with “python”), remember to change image_dir to country or décor directory path;

6.<optional> run tensorboard by typing <tensorboard --logdir tf_files/training_summaries &> in terminal to have a view at learning in the browser ;


experiments:

retrain.py won’t allow to do multiclass classification, so experiments are done by creating 2 separate classifiers, one for countries and one for décor. 

Experiments has numbers like (1) with corresponds to summaries directories and retrained graphs like  retrained_graph1.pb with is, as name said, retrained graph for first (1) experiment. Keeping this convention make it easy to analyse training data in tensorboard

due to imbalanced class distribution in country classification, setting --validation_batch_size to -1, tensorflow still point out that Belarus has less then 20 images;

experiments were conducted using mobilnet_0.50_128 architecture due to its low compute time

!change image_dir option to
directories that were created using data_manipulation.py script
<path to country directory> example: /foo/bar/country
<path to decor directory> example: /foo/bar/decor

classify by country

first(1) run parameters:

python -m scripts.retrain --bottleneck_dir=tf_files/bottlenecks --how_many_training_steps=500 --model_dir=tf_files/models/ --summaries_dir=tf_files/training_summaries/1 --output_graph=tf_files/retrained_graph1.pb --output_labels=tf_files/retrained_labels1.txt --architecture=mobilenet_0.50_128 --validation_batch_size=-1 --image_dir=<path to country directory>
 
with result in 95.8% accuracy, after looking at tensorboard its possibly due to overfit 

second(2) run parameters:

python -m scripts.retrain --bottleneck_dir=tf_files/bottlenecks --how_many_training_steps=500 --model_dir=tf_files/models/ --summaries_dir=tf_files/training_summaries/2 --output_graph=tf_files/retrained_graph2.pb --output_labels=tf_files/retrained_labels2.txt --architecture=mobilenet_0.50_128 --validation_batch_size=-1 --image_dir=<path to country directory> --flip_left_right --random_crop=10 --random_scale=10 --random_brightness=15

this time some augmentation option are on, model is still overfiting with accuracy 95%

third(3) run parameters:

python -m scripts.retrain --bottleneck_dir=tf_files/bottlenecks --how_many_training_steps=500 --model_dir=tf_files/models/ --summaries_dir=tf_files/training_summaries/3 --output_graph=tf_files/retrained_graph3.pb --output_labels=tf_files/retrained_labels3.txt --architecture=mobilenet_0.50_128 --validation_batch_size=-1 --image_dir=<path to country directory> --flip_left_right --random_crop=10 --random_scale=10 --random_brightness=15 --learning_rate=0.005
 
this time learning_rate was set to 0.005, half the default value. Accuracy fell to 91%, but learning process looks more stable.


classify by decor:

first(4) run parameters: 

python -m scripts.retrain --bottleneck_dir=tf_files/bottlenecks --how_many_training_steps=500 --model_dir=tf_files/models/ --summaries_dir=tf_files/training_summaries/4 --output_graph=tf_files/retrained_graph4.pb --output_labels=tf_files/retrained_labels4.txt --architecture=mobilenet_0.50_128 --validation_batch_size=-1 --image_dir=<path to decor> 

as seen in tensorboard, model stopped learning before 200 steps, possible overfit, accuracy 71.4%

second(5) run parameters:

python -m scripts.retrain --bottleneck_dir=tf_files/bottlenecks --how_many_training_steps=500 --model_dir=tf_files/models/ --summaries_dir=tf_files/training_summaries/5 --output_graph=tf_files/retrained_graph5.pb --output_labels=tf_files/retrained_labels5.txt --architecture=mobilenet_0.50_128 --validation_batch_size=-1 --image_dir=<path to decor>  --flip_left_right --random_crop=10 --random_scale=10 --random_brightness=15

similar accuracy, 70%, augmentations haven't give any advancement,

third(6) run parameters:

python -m scripts.retrain --bottleneck_dir=tf_files/bottlenecks --how_many_training_steps=500 --model_dir=tf_files/models/ --summaries_dir=tf_files/training_summaries/6 --output_graph=tf_files/retrained_graph6.pb --output_labels=tf_files/retrained_labels6.txt --architecture=mobilenet_0.50_128 --validation_batch_size=-1 --image_dir=<path to decor> --flip_left_right --random_crop=10 --random_scale=10 --random_brightness=15 --learning_rate=0.005

lowering learning_rate worsen accuracy to 68%, maybe increasing  how_many_training_steps would help
