-The pretrained model must be downloaded in the <git-repository-path>/model-training/models folder.
-We are currently using "multi_cased_L-12_H-768_A-12" model
-It can be downloaded from "https://storage.googleapis.com/bert_models/2018_11_23/multi_cased_L-12_H-768_A-12.zip"
[source- https://github.com/google-research/bert/blob/master/README.md].


-To run the bert-server to access the pretrained model.
      -Go into directory <git-repository-path>/model-training/models.
      -To serve bert model we use [bert-serving-start -model_dir ./multi_cased_L-12_H-768_A-12/ -num_worker=1 -show_tokens_to_client] command