CUDA_VISIBLE_DEVICES=1 python3 test.py ckpt_path=trained/first_training_f-rcnn_inception_v2/inference/frozen_inference_graph.pb labels_path=data/wildlife_label_map.pbtxt file_name=videos/bear_zoo_180529_0.MPG save_file_name=results/first_training_f-rcnn_inception_v2/bear_zoo_180529_0.mkv n_frames=0 batch_size=25

CUDA_VISIBLE_DEVICES=1 python3 test.py ckpt_path=trained/first_training_f-rcnn_inception_v2/inference/frozen_inference_graph.pb labels_path=data/wildlife_label_map.pbtxt file_name=videos/bear_zoo_180529_1.MPG save_file_name=results/first_training_f-rcnn_inception_v2/bear_zoo_180529_1.mkv n_frames=0 batch_size=25

CUDA_VISIBLE_DEVICES=1 python3 test.py ckpt_path=trained/first_training_f-rcnn_inception_v2/inference/frozen_inference_graph.pb labels_path=data/wildlife_label_map.pbtxt file_name=videos/bear_zoo_180529_2.MPG save_file_name=results/first_training_f-rcnn_inception_v2/bear_zoo_180529_2.mkv n_frames=0 batch_size=25