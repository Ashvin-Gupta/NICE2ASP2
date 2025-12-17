Looking at the clinical guideline text, I'll extract the ASP rules for each section:

% [1.1.1]
offer("pancreatic protocol CT") :- have("obstructive jaundice"), suspected("pancreatic cancer"), not drain("bile duct").
fired("1.1.1") :- have("obstructive jaundice"), suspected("pancreatic cancer"), not drain("bile duct").

% [1.1.2]
1{offer("FDG-PET/CT"); offer("EUS", "EUS-guided tissue sampling")}2 :- have("obstructive jaundice"), suspected("pancreatic cancer"), offered("pancreatic protocol CT"), findings("pancreatic protocol CT", "unclear diagnosis").
fired("1.1.2") :- have("obstructive jaundice"), suspected("pancreatic cancer"), offered("pancreatic protocol CT"), findings("pancreatic protocol CT", "unclear diagnosis").

% [1.1.3]
take("biliary brushing", "cytology") :- relieve("biliary obstruction"), have("no tissue diagnosis").
fired("1.1.3") :- relieve("biliary obstruction"), have("no tissue diagnosis").

% [1.1.4]
offer("pancreatic protocol CT") :- have("pancreatic abnormalities"), not have("jaundice").
fired("1.1.4") :- have("pancreatic abnormalities"), not have("jaundice").

% [1.1.5]
1{offer("FDG-PET/CT"); offer("EUS", "EUS-guided tissue sampling")}2 :- have("pancreatic abnormalities"), not have("jaundice"), offered("pancreatic protocol CT"), findings("pancreatic protocol CT", "unclear diagnosis").
fired("1.1.5") :- have("pancreatic abnormalities"), not have("jaundice"), offered("pancreatic protocol CT"), findings("pancreatic protocol CT", "unclear diagnosis").

% [1.1.6]
offer("EUS", "EUS-guided tissue sampling") :- need("cytological or histological samples").
fired("1.1.6") :- need("cytological or histological samples").

% [1.1.7]
1{offer("pancreatic protocol CT"); offer("MRI/MRCP")}1 :- have("pancreatic cysts").
fired("1.1.7") :- have("pancreatic cysts").
offer("MRI/MRCP") :- have("pancreatic cysts"), offered("pancreatic protocol CT"), need("more information").
fired("1.1.7_B") :- have("pancreatic cysts"), offered("pancreatic protocol CT"), need("more information").
offer("pancreatic protocol CT") :- have("pancreatic cysts"), offered("MRI/MRCP"), need("more information").
fired("1.1.7_C") :- have("pancreatic cysts"), offered("MRI/MRCP"), need("more information").

% [1.1.8]
refer("resection") :- have("obstructive jaundice"), have("cystic lesions in the head of the pancreas").
fired("1.1.8") :- have("obstructive jaundice"), have("cystic lesions in the head of the pancreas").
refer("resection") :- have("enhancing solid component in the cyst").
fired("1.1.8_B") :- have("enhancing solid component in the cyst").
refer("resection") :- have("main pancreatic duct that is 10 mm diameter or larger").
fired("1.1.8_C") :- have("main pancreatic duct that is 10 mm diameter or larger").

% [1.1.9]
offer("EUS") :- have("pancreatic cysts"), offered("pancreatic protocol CT"), offered("MRI/MRCP"), need("more information on the likelihood of malignancy").
fired("1.1.9") :- have("pancreatic cysts"), offered("pancreatic protocol CT"), offered("MRI/MRCP"), need("more information on the likelihood of malignancy").
offer("EUS") :- have("pancreatic cysts"), offered("pancreatic protocol CT"), offered("MRI/MRCP"), need("unclear whether surgery is needed").
fired("1.1.9_B") :- have("pancreatic cysts"), offered("pancreatic protocol CT"), offered("MRI/MRCP"), need("unclear whether surgery is needed").

% [1.1.10]
consider("EUS", "fine-needle aspiration") :- need("more information on the likelihood of malignancy").
fired("1.1.10") :- need("more information on the likelihood of malignancy").

% [1.1.11]
perform("CEA assay") :- offered("fine-needle aspiration"), have("sufficient sample").
fired("1.1.11") :- offered("fine-needle aspiration"), have("sufficient sample").
perform("cytology") :- offered("fine-needle aspiration").
fired("1.1.11_B") :- offered("fine-needle aspiration").

% [1.1.14]
offer("surveillance", "pancreatic cancer") :- have("inherited high risk"), have("hereditary pancreatitis"), have("PRSS1").
fired("1.1.14") :- have("inherited high risk"), have("hereditary pancreatitis"), have("PRSS1").
offer("surveillance", "pancreatic cancer") :- have("inherited high risk"), 1{have("BRCA1"); have("BRCA2"); have("PALB2"); have("CDKN2A (p16)")}4, first_degree_relative("pancreatic cancer", _).
fired("1.1.14_B") :- have("inherited high risk"), 1{have("BRCA1"); have("BRCA2"); have("PALB2"); have("CDKN2A (p16)")}4, first_degree_relative("pancreatic cancer", _).
offer("surveillance", "pancreatic cancer") :- have("inherited high risk"), have("Peutz–Jeghers syndrome").
fired("1.1.14_C") :- have("inherited high risk"), have("Peutz–Jeghers syndrome").

% [1.1.15]
consider("surveillance", "pancreatic cancer") :- have("inherited high risk"), first_degree_relative("pancreatic cancer", X), first_degree_relative("pancreatic cancer", Y), X!=Y.
fired("1.1.15") :- have("inherited high risk"), first_degree_relative("pancreatic cancer", X), first_degree_relative("pancreatic cancer", Y), X!=Y.
consider("surveillance", "pancreatic cancer") :- have("inherited high risk"), have("Lynch syndrome"), first_degree_relative("pancreatic cancer", _).
fired("1.1.15_B") :- have("inherited high risk"), have("Lynch syndrome"), first_degree_relative("pancreatic cancer", _).

% [1.1.16]
1{consider("MRI/MRCP"); consider("EUS")}1 :- have("inherited high risk"), not have("hereditary pancreatitis").
fired("1.1.16") :- have("inherited high risk"), not have("hereditary pancreatitis").

% [1.1.17]
consider("pancreatic protocol CT") :- have("inherited high risk"), have("hereditary pancreatitis"), have("PRSS1").
fired("1.1.17") :- have("inherited high risk"), have("hereditary pancreatitis"), have("PRSS1").

% [1.1.18]
:- have("inherited high risk"), offer("EUS"), have("hereditary pancreatitis").
fired("1.1.18").
constraint_ok("1.1.18").

% [1.3.1]
offer("pancreatic protocol CT") :- have("pancreatic cancer"), not offered("pancreatic protocol CT").
fired("1.3.1") :- have("pancreatic cancer"), not offered("pancreatic protocol CT").

% [1.3.2]
offer("FDG-PET/CT") :- have("localised disease"), 1{offer("surgery"); offer("radiotherapy"); offer("systemic therapy")}3.
fired("1.3.2") :- have("localised disease"), 1{offer("surgery"); offer("radiotherapy"); offer("systemic therapy")}3.

% [1.3.3]
consider("MRI") :- suspected("liver metastases"), need("more information").
fired("1.3.3") :- suspected("liver metastases"), need("more information").
consider("EUS") :- need("more information"), need("tumour and node staging").
fired("1.3.3_B") :- need("more information"), need("tumour and node staging").
consider("laparoscopy", "laparoscopic ultrasound") :- suspected("peritoneal"), offer("resectional surgery").
fired("1.3.3_C") :- suspected("peritoneal"), offer("resectional surgery").
consider("laparoscopy", "laparoscopic ultrasound") :- suspected("liver metastases"), offer("resectional surgery").
fired("1.3.3_D") :- suspected("liver metastases"), offer("resectional surgery").

% [1.13.2]
assess("additional symptoms") :- have("weight loss", "unexplained").
fired("1.13.2") :- have("weight loss", "unexplained").
1{offer("urgent investigation"); offer("suspected cancer pathway referral")}1 :- have("weight loss", "unexplained").
fired("1.13.2_B") :- have("weight loss", "unexplained").

% [1.13.3]
assess("additional symptoms") :- have("appetite loss", "unexplained").
fired("1.13.3") :- have("appetite loss", "unexplained").
1{offer("urgent investigation"); offer("suspected cancer pathway referral")}1 :- have("appetite loss", "unexplained").
fired("1.13.3_B") :- have("appetite loss", "unexplained").

% [1.2.4]
refer("suspected cancer pathway referral", "pancreatic cancer") :- age(X), X>=40, have("jaundice").
fired("1.2.4") :- age(X), X>=40, have("jaundice").

% [1.2.5]
consider("CT") :- age(X), X>=60, have("weight loss"), 1{have("diarrhoea"); have("back pain"); have("abdominal pain"); have("nausea"); have("vomiting"); have("constipation"); have("new-onset diabetes")}7.
fired("1.2.5") :- age(X), X>=60, have("weight loss"), 1{have("diarrhoea"); have("back pain"); have("abdominal pain"); have("nausea"); have("vomiting"); have("constipation"); have("new-onset diabetes")}7.
consider("ultrasound") :- age(X), X>=60, have("weight loss"), 1{have("diarrhoea"); have("back pain"); have("abdominal pain"); have("nausea"); have("vomiting"); have("constipation"); have("new-onset diabetes")}7, not available("CT").
fired("1.2.5_B") :- age(X), X>=60, have("weight loss"), 1{have("diarrhoea"); have("back pain"); have("abdominal pain"); have("nausea"); have("vomiting"); have("constipation"); have("new-onset diabetes")}7, not available("CT").

#show fired/1.
#show constraint_ok/1.