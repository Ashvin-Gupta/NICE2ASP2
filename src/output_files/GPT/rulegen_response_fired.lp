% [1.1.1]
offer("pancreatic protocol CT scan") :- have("obstructive jaundice"), have("suspected pancreatic cancer").
fired("1.1.1") :- have("obstructive jaundice"), have("suspected pancreatic cancer").

% [1.1.2]
1{offer("FDG-PET/CT"); offer("endoscopic ultrasound (EUS)"); offer("EUS-guided tissue sampling")}3 :- have("obstructive jaundice"), have("suspected pancreatic cancer"), offered("pancreatic protocol CT scan"), findings("pancreatic protocol CT scan","diagnosis is still unclear").
fired("1.1.2") :- have("obstructive jaundice"), have("suspected pancreatic cancer"), offered("pancreatic protocol CT scan"), findings("pancreatic protocol CT scan","diagnosis is still unclear").

% [1.1.3]
offer("biliary brushing") :- have("obstructive jaundice"), used_for("endoscopic retrograde cholangiopancreatography (ERCP)","biliary obstruction"), findings("biliary brushing","no tissue diagnosis").
fired("1.1.3") :- have("obstructive jaundice"), used_for("endoscopic retrograde cholangiopancreatography (ERCP)","biliary obstruction"), findings("biliary brushing","no tissue diagnosis").

% [1.1.4]
offer("pancreatic protocol CT scan") :- have("pancreatic abnormalities"), not have("jaundice").
fired("1.1.4") :- have("pancreatic abnormalities"), not have("jaundice").

% [1.1.5]
1{offer("FDG-PET/CT"); offer("endoscopic ultrasound (EUS)"); offer("EUS-guided tissue sampling")}3 :- have("pancreatic abnormalities"), not have("jaundice"), offered("pancreatic protocol CT scan"), findings("pancreatic protocol CT scan","diagnosis is still unclear").
fired("1.1.5") :- have("pancreatic abnormalities"), not have("jaundice"), offered("pancreatic protocol CT scan"), findings("pancreatic protocol CT scan","diagnosis is still unclear").

% [1.1.6]
offer("endoscopic ultrasound (EUS)") :- findings("endoscopic ultrasound (EUS)","cytological or histological samples are needed").
fired("1.1.6") :- findings("endoscopic ultrasound (EUS)","cytological or histological samples are needed").
offer("EUS-guided tissue sampling") :- findings("endoscopic ultrasound (EUS)","cytological or histological samples are needed").
fired("1.1.6_B") :- findings("endoscopic ultrasound (EUS)","cytological or histological samples are needed").

% [1.1.7]
1{offer("pancreatic protocol CT scan"); offer("MRI/MRCP")}2 :- have("pancreatic cysts").
fired("1.1.7") :- have("pancreatic cysts").
offer("MRI/MRCP") :- have("pancreatic cysts"), offered("pancreatic protocol CT scan"), findings("pancreatic protocol CT scan","more information is needed").
fired("1.1.7_B") :- have("pancreatic cysts"), offered("pancreatic protocol CT scan"), findings("pancreatic protocol CT scan","more information is needed").
offer("pancreatic protocol CT scan") :- have("pancreatic cysts"), offered("MRI/MRCP"), findings("MRI/MRCP","more information is needed").
fired("1.1.7_C") :- have("pancreatic cysts"), offered("MRI/MRCP"), findings("MRI/MRCP","more information is needed").

% [1.1.8]
high_risk_feature("high-risk features","cystic lesions in the head of the pancreas") :- have("pancreatic cysts"), have("cystic lesions in the head of the pancreas"), have("obstructive jaundice").
fired("1.1.8") :- have("pancreatic cysts"), have("cystic lesions in the head of the pancreas"), have("obstructive jaundice").
high_risk_feature("high-risk features","enhancing solid component in the cyst") :- have("pancreatic cysts"), have("enhancing solid component in the cyst").
fired("1.1.8_B") :- have("pancreatic cysts"), have("enhancing solid component in the cyst").
high_risk_feature("high-risk features","a main pancreatic duct that is 10 mm diameter or larger") :- have("pancreatic cysts"), have("a main pancreatic duct that is 10 mm diameter or larger").
fired("1.1.8_C") :- have("pancreatic cysts"), have("a main pancreatic duct that is 10 mm diameter or larger").

refer("resection","pancreatic cancer") :- have("pancreatic cysts"), high_risk_feature("high-risk features","cystic lesions in the head of the pancreas").
fired("1.1.8_D") :- have("pancreatic cysts"), high_risk_feature("high-risk features","cystic lesions in the head of the pancreas").
refer("resection","pancreatic cancer") :- have("pancreatic cysts"), high_risk_feature("high-risk features","enhancing solid component in the cyst").
fired("1.1.8_E") :- have("pancreatic cysts"), high_risk_feature("high-risk features","enhancing solid component in the cyst").
refer("resection","pancreatic cancer") :- have("pancreatic cysts"), high_risk_feature("high-risk features","a main pancreatic duct that is 10 mm diameter or larger").
fired("1.1.8_F") :- have("pancreatic cysts"), high_risk_feature("high-risk features","a main pancreatic duct that is 10 mm diameter or larger").

% [1.1.9]
offer("endoscopic ultrasound (EUS)") :- have("pancreatic cysts"), offered("pancreatic protocol CT scan"), offered("MRI/MRCP"), findings("pancreatic protocol CT scan","more information is needed on the likelihood of malignancy").
fired("1.1.9") :- have("pancreatic cysts"), offered("pancreatic protocol CT scan"), offered("MRI/MRCP"), findings("pancreatic protocol CT scan","more information is needed on the likelihood of malignancy").
offer("endoscopic ultrasound (EUS)") :- have("pancreatic cysts"), offered("pancreatic protocol CT scan"), offered("MRI/MRCP"), findings("MRI/MRCP","more information is needed on the likelihood of malignancy").
fired("1.1.9_B") :- have("pancreatic cysts"), offered("pancreatic protocol CT scan"), offered("MRI/MRCP"), findings("MRI/MRCP","more information is needed on the likelihood of malignancy").
offer("endoscopic ultrasound (EUS)") :- have("pancreatic cysts"), offered("pancreatic protocol CT scan"), offered("MRI/MRCP"), findings("pancreatic protocol CT scan","it is not clear whether surgery is needed").
fired("1.1.9_C") :- have("pancreatic cysts"), offered("pancreatic protocol CT scan"), offered("MRI/MRCP"), findings("pancreatic protocol CT scan","it is not clear whether surgery is needed").
offer("endoscopic ultrasound (EUS)") :- have("pancreatic cysts"), offered("pancreatic protocol CT scan"), offered("MRI/MRCP"), findings("MRI/MRCP","it is not clear whether surgery is needed").
fired("1.1.9_D") :- have("pancreatic cysts"), offered("pancreatic protocol CT scan"), offered("MRI/MRCP"), findings("MRI/MRCP","it is not clear whether surgery is needed").

% [1.1.10]
consider("fine-needle aspiration") :- have("pancreatic cysts"), offered("endoscopic ultrasound (EUS)"), findings("endoscopic ultrasound (EUS)","likelihood of malignancy").
fired("1.1.10") :- have("pancreatic cysts"), offered("endoscopic ultrasound (EUS)"), findings("endoscopic ultrasound (EUS)","likelihood of malignancy").

% [1.1.11]
used_for("fine-needle aspiration","carcinoembryonic antigen (CEA) assay") :- offered("fine-needle aspiration"), findings("fine-needle aspiration","sufficient sample").
fired("1.1.11") :- offered("fine-needle aspiration"), findings("fine-needle aspiration","sufficient sample").
offer("carcinoembryonic antigen (CEA) assay") :- offered("fine-needle aspiration"), findings("fine-needle aspiration","sufficient sample").
fired("1.1.11_B") :- offered("fine-needle aspiration"), findings("fine-needle aspiration","sufficient sample").

% [1.1.12]
staging_for("staging","pancreatic cancer") :- have("cysts that are thought to be malignant").
fired("1.1.12") :- have("cysts that are thought to be malignant").

% [1.1.13]
ask("first-degree relatives","pancreatic cancer") :- have("pancreatic cancer").
fired("1.1.13") :- have("pancreatic cancer").

% [1.1.14]
offer("pancreatic cancer surveillance") :- have("hereditary pancreatitis"), have("PRSS1").
fired("1.1.14") :- have("hereditary pancreatitis"), have("PRSS1").
offer("pancreatic cancer surveillance") :- 1{have("BRCA1"); have("BRCA2"); have("PALB2"); have("CDKN2A (p16)")}4, first_degree_relative("pancreatic cancer",_).
fired("1.1.14_B") :- 1{have("BRCA1"); have("BRCA2"); have("PALB2"); have("CDKN2A (p16)")}4, first_degree_relative("pancreatic cancer",_).
offer("pancreatic cancer surveillance") :- have("Peutz–Jeghers syndrome").
fired("1.1.14_C") :- have("Peutz–Jeghers syndrome").

% [1.1.15]
offer("pancreatic cancer surveillance") :- have("2 or more first-degree relatives with pancreatic cancer, across 2 or more generations").
fired("1.1.15") :- have("2 or more first-degree relatives with pancreatic cancer, across 2 or more generations").
offer("pancreatic cancer surveillance") :- have("Lynch syndrome"), 1{have("MLH1"); have("MSH2"); have("MSH6"); have("PMS2")}4, first_degree_relative("pancreatic cancer",_).
fired("1.1.15_B") :- have("Lynch syndrome"), 1{have("MLH1"); have("MSH2"); have("MSH6"); have("PMS2")}4, first_degree_relative("pancreatic cancer",_).

% [1.1.16]
consider("MRI/MRCP") :- offer("pancreatic cancer surveillance"), have("people without hereditary pancreatitis").
fired("1.1.16") :- offer("pancreatic cancer surveillance"), have("people without hereditary pancreatitis").
consider("endoscopic ultrasound (EUS)") :- offer("pancreatic cancer surveillance"), have("people without hereditary pancreatitis").
fired("1.1.16_B") :- offer("pancreatic cancer surveillance"), have("people without hereditary pancreatitis").

% [1.1.17]
consider("pancreatic protocol CT scan") :- offer("pancreatic cancer surveillance"), have("hereditary pancreatitis"), have("PRSS1").
fired("1.1.17") :- offer("pancreatic cancer surveillance"), have("hereditary pancreatitis"), have("PRSS1").

% [1.1.18]
:- offer("endoscopic ultrasound (EUS)"), have("hereditary pancreatitis").
fired("1.1.18").
constraint_ok("1.1.18").

% [1.3.1]
offer("pancreatic protocol CT scan") :- have("newly diagnosed pancreatic cancer"), not offered("pancreatic protocol CT scan").
fired("1.3.1") :- have("newly diagnosed pancreatic cancer"), not offered("pancreatic protocol CT scan").
used_for("pancreatic protocol CT scan","chest") :- have("newly diagnosed pancreatic cancer"), offered("pancreatic protocol CT scan").
fired("1.3.1_B") :- have("newly diagnosed pancreatic cancer"), offered("pancreatic protocol CT scan").
used_for("pancreatic protocol CT scan","abdomen") :- have("newly diagnosed pancreatic cancer"), offered("pancreatic protocol CT scan").
fired("1.3.1_C") :- have("newly diagnosed pancreatic cancer"), offered("pancreatic protocol CT scan").
used_for("pancreatic protocol CT scan","pelvis") :- have("newly diagnosed pancreatic cancer"), offered("pancreatic protocol CT scan").
fired("1.3.1_D") :- have("newly diagnosed pancreatic cancer"), offered("pancreatic protocol CT scan").

% [1.3.2]
offer("FDG-PET/CT") :- have("pancreatic cancer"), findings("pancreatic protocol CT scan","localised disease on CT"), 1{treatment_for("surgery","pancreatic cancer"); treatment_for("radiotherapy","pancreatic cancer"); treatment_for("systemic therapy","pancreatic cancer")}3.
fired("1.3.2") :- have("pancreatic cancer"), findings("pancreatic protocol CT scan","localised disease on CT"), 1{treatment_for("surgery","pancreatic cancer"); treatment_for("radiotherapy","pancreatic cancer"); treatment_for("systemic therapy","pancreatic cancer")}3.

% [1.3.3]
consider("MRI") :- have("pancreatic cancer"), findings("pancreatic protocol CT scan","suspected liver metastases").
fired("1.3.3") :- have("pancreatic cancer"), findings("pancreatic protocol CT scan","suspected liver metastases").
consider("endoscopic ultrasound (EUS)") :- have("pancreatic cancer"), findings("endoscopic ultrasound (EUS)","tumour and node staging").
fired("1.3.3_B") :- have("pancreatic cancer"), findings("endoscopic ultrasound (EUS)","tumour and node staging").
consider("laparoscopy") :- have("pancreatic cancer"), findings("laparoscopic ultrasound","suspected small-volume peritoneal and/or liver metastases"), have("resectional surgery").
fired("1.3.3_C") :- have("pancreatic cancer"), findings("laparoscopic ultrasound","suspected small-volume peritoneal and/or liver metastases"), have("resectional surgery").
consider("laparoscopic ultrasound") :- have("pancreatic cancer"), findings("laparoscopic ultrasound","suspected small-volume peritoneal and/or liver metastases"), have("resectional surgery").
fired("1.3.3_D") :- have("pancreatic cancer"), findings("laparoscopic ultrasound","suspected small-volume peritoneal and/or liver metastases"), have("resectional surgery").

% [1.13.2]
assessment_for("urgent investigation","additional symptoms, signs or findings that may help to clarify which cancer is most likely") :- have("unexplained weight loss").
fired("1.13.2") :- have("unexplained weight loss").
offer("urgent investigation") :- have("unexplained weight loss").
fired("1.13.2_B") :- have("unexplained weight loss").
offer("suspected cancer pathway referral") :- have("unexplained weight loss").
fired("1.13.2_C") :- have("unexplained weight loss").

% [1.13.3]
assessment_for("urgent investigation","additional symptoms, signs or findings that may help to clarify which cancer is most likely") :- have("unexplained appetite loss").
fired("1.13.3") :- have("unexplained appetite loss").
offer("urgent investigation") :- have("unexplained appetite loss").
fired("1.13.3_B") :- have("unexplained appetite loss").
offer("suspected cancer pathway referral") :- have("unexplained appetite loss").
fired("1.13.3_C") :- have("unexplained appetite loss").

% [1.2.4]
refer("suspected cancer pathway referral","pancreatic cancer") :- age(X), have("jaundice"), X>=40.
fired("1.2.4") :- age(X), have("jaundice"), X>=40.

% [1.2.5]
consider("CT") :- age(X), have("weight loss"), 1{have("diarrhoea"); have("back pain"); have("abdominal pain"); have("nausea"); have("vomiting"); have("constipation"); have("new-onset diabetes")}7, X>=60.
fired("1.2.5") :- age(X), have("weight loss"), 1{have("diarrhoea"); have("back pain"); have("abdominal pain"); have("nausea"); have("vomiting"); have("constipation"); have("new-onset diabetes")}7, X>=60.
consider("ultrasound") :- age(X), have("weight loss"), 1{have("diarrhoea"); have("back pain"); have("abdominal pain"); have("nausea"); have("vomiting"); have("constipation"); have("new-onset diabetes")}7, X>=60, not available("CT").
fired("1.2.5_B") :- age(X), have("weight loss"), 1{have("diarrhoea"); have("back pain"); have("abdominal pain"); have("nausea"); have("vomiting"); have("constipation"); have("new-onset diabetes")}7, X>=60, not available("CT").

#show fired/1.
#show constraint_ok/1.