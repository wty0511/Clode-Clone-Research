# Code-Clone-Research
file name(data) | description
------------ | -------------
genealogy | genealogy of each project
maximum_entropy_model | 10 maximum entropy models
technical_debt_dataset.csv|public dataset of SATDs
pr.csv|link of git repository
commit_message.dic|commit message(title and body)of each code clone
commit_message_clean.dic|commit message after data cleaning
commit_message_clean_preprocess.dic|commit message after data preprocessing
commit_message_in_pr.dic|commit message in pull request
commit_message_in_pr_cleaning.dic|commit message in pull request afterdata cleaning
commit_message_in_pr_cleaning_<br/>preprocess.dic|commit message in pull request after preprocessing
code_comment(SATD).dic|code comment in code clone(multi linecomment and single line comment)Self Admitted technical Debts are labeled
code_comment_clean.dic|code comment in code clone after data cleaning
code_comment_clean_preprocessing.dic|code comment in code clone after preprocessing
pr_message(path).dic|contain title, body, reviews, issue comments and review comments of pull request, also the  path of git repository, you can find the repository of each project.
pr_message(NL).dic|contain title, body, reviews, issue comments and review comments of pull request
pr_clean.dic|pull request after data cleaning
pr_clean_preprocessing.dic|all natural language in pull request (except commit message) after preporcessing
pr_preprocess.dic|all natural language in pull request(title, body, reviews, issue comments and review comments, commit messages) after preporcessing
pr_all_message.dic|all message related to pull request: "pr_info":(basic information of pull request), "reviews","issue_comments", "review_comments", "commit_id", "issue_envent", "file"(files changed), "timeline_event","reactions",checks and the project of pull requests are not collected
code.dic|all code clones
code_pre_15.dic|code block before the code clone(at least 15 lines)
SATD.csv|all Self Admitted technical Debts after data cleaning
commit_pr(final version).dic|pull request related to each commit
emoj.txt|emoj that need to be removed
html.txt|all html tags need to be removed
code_comment_label.csv|remove all code in code comment, "text" is the original comment, "to" is one after removal
technical_debt_dataset.csv|public dataset of SATDs
technical_debt_dataset_clean.csv|public dataset of SATDs after data cleaning|
frequency_bigramdictionary_en_243_342.txt|used when doing spelling check
frequency_dictionary_en_82_765.txt|used when doing spelling check

data are saved in google drive
https://drive.google.com/drive/folders/1oO2DkGoRBr1iXH45_5eLIwyp7mcUy-lV


file name(scipt) | description
------------ | -------------
classify_comment.py| predict SATDs
SATD_stat.py|get the life cycle of SATDs
preprocessing.py| preprocessing for commit message, code comment and pull request
pr_cleaning.py|data cleaning for pull request
LDA.py|topic modeling
LDA_optimize.py| get optimal topic number
LDA.R|topic modeling
LDA_optimize.R| get optimal topic number
getComment.py| get code comment in code clone
getCode.py| get code clone
get_pr_number.py| get pull request number of each commit
get_pr_message.py| get all messages in pull request
get_issues.py| get commit of pull request(can not find using git)
get_commit_message_pr.py|get commit of pull request
get_histoy_SATD.py| get history of SATD
get_future_SATD.py|  get future version of SATD
get_commit_message.py| get commit message of code clone
get_comment_pre_15.py| get code comment before code clone
commit_message_cleaning.py| data cleaning of commit message
comment_classifier.py| train classfier of SATD
code_comment_clean.py| data cleaning of code comment
Twitter-LDA-master|Twitter-LDA

hyper-parameter of topic modeling can be found in Matics 2021.9.15.pptx
use lda(tf-idf) for pull request
use twitter lda for commit message and code comment
