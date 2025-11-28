% 1.1.1
offer("pancreatic protocol CT scan") :- have("obstructive jaundice"), have("suspected pancreatic cancer").  
offer("draining bile duct") :- offered("pancreatic protocol CT scan"), have("obstructive jaundice"), have("suspected pancreatic cancer").
% 1.1.2                          
1 {offer("FDG-PET/CT"); offer("EUS-guided tissue sampling")} 2 :- findings("pancreatic protocol CT scan","diagnosis is still unclear"), offered("pancreatic protocol CT scan"), have("obstructive jaundice").
% 1.1.3
offer("biliary brushing") :- findings("EUS-guided tissue sampling","no tissue diagnosis"), offer("ERCP", "bilary obstruction"), have("obstructive jaundice").
% 1.1.4
offer("pancreatic protocol CT scan") :- have("pancreatic abnormalities"), not have("jaundice").
% 1.1.5
1 {offer("FDG-PET/CT"); offer("EUS-guided tissue sampling")} 2 :- findings("pancreatic protocol CT scan","diagnosis is still unclear"), offered("pancreatic protocol CT scan"), have("pancreatic abnormalities"), not have("jaundice").
% 1.1.6
offer("EUS-guided tissue sampling") :- 1{need("cytological samples"); need("histological samples")}2, have("pancreatic abnormalities"), not have("jaundice").
% 1.1.7
1{ offer("pancreatic protocol CT scan"); offer("MRI/MRCP")} 1 :- have("pancreatic cysts").
offer("pancreatic protocol CT scan") :- offered("MRI/MRCP"), need("more information"), have("pancreatic cysts").
offer("MRI/MRCP") :- offered("pancreatic protocol CT scan"), need("more information"), have("pancreatic cysts").
% 1.1.8
refer("resection") :- have("obstructive jaundice"), findings("cystic lesions", "head of pancreas"), have("pancreatic cysts").
refer("resection") :- findings("solid component", "pancreatic cyst"), have("pancreatic cysts").
refer("resection") :- findings("10mm", "pancreatic duct"), have("pancreatic cysts").
% 1.1.9
offer("EUS") :- offered("pancreatic protocol CT scan"), offered("MRI/MRCP"), 1{need("maligancy likelihood"); need("info on surgery")}2, have("pancreatic cysts").
% 1.1.10
consider("fine-needle", "EUS") :- need("maligancy likelihood"), have("pancreatic cysts"), offered("EUS").
% 1.1.11
1{offer("CEA assay"); offer("cytology")} 1 :- offered("fine needle"), sufficient sample, have("pancreatic cysts").
% 1.1.12
follow("staging recommendations") :- findings("malignancy", "pancreatic cysts"), have("pancreatic cysts").
% 1.1.13  
ask("family history") :- have(cancer("pancreas")).
address("inherited risk concerns") :- have(cancer("pancreas")), first_degree_relative(cancer("pancreas"), _).
% 1.1.14
offer("surveillance", cancer("pancreas")) :- have("hereditary pancreatitis"), have("PRSS1"), have("inherited high risk").
offer("surveillance", cancer("pancreas")) :- 1{have("BRCA1");have("BRCA2");have("PALB2");have("CDKN2A")}4, first_degree_relative(cancer("pancreas"),_), have("inherited high risk").
offer("surveillance", cancer("pancreas")) :- have("peutz jeghers"), have("inherited high risk").
% 1.1.15
consider("surveillance", cancer("pancreas")) :- have("lynch syndrome"), first_degree_relative(cancer("pancreas"),_), have("inherited high risk").
consider("surveillance", cancer("pancreas")) :- first_degree_relative(cancer("pancreas"),X), first_degree_relative(cancer("pancreas"),Y), X!=Y, have("inherited high risk").
% 1.1.16
1{ consider("MRI/MRCP"); consider("EUS")} 1 :-  not have("hereditary pancreatitis"), offer("surveillance", cancer("pancreas")), have("inherited high risk").
% 1.1.17
consider("pancreatic protocol CT scan") :- have("hereditary pancreatitis"), have("PRSS1"), offer("surveillance", cancer("pancreas")), have("inherited high risk").
% 1.1.18
:- offer("EUS"), have("hereditary pancreatitis"), have("inherited high risk").
% 1.3.1
3{offer("pancreatic protocol CT scan", "chest"); offer("pancreatic protocol CT scan", "abdomen"); offer("pancreatic protocol CT scan", "pelvis")} 3 :- have(cancer("pancreas")), not offered("pancreatic protocol CT scan").
% 1.3.2
offer("FDG-PET/CT") :- 1{treatment("surgery"); treatment("radiotherapy"); treatment("systemic therapy")}3, findings_from_procedure("pancreatic protocol CT scan", "localised disease"). 
% 1.3.3
consider("MRI/MRCP") :-  need("more information"), suspected("liver metastases").
consider("endoscopic ultrasound") :-  need("more information"), need("tumor staging"), need("node staging").
consider("lacroscpoic ultrasound") :- suspected("small volume peritoneal"), susptected("liver metastases"), possible("resectional surgery").
% 1.2.4
refer("suspected cancer pathway", cancer("pancreas")) :- age(X), have("jaundice"), X>=40.
% 1.2.5
consider("CT scan") :- age(X), have("unexplained weight loss"), 1{have("diarrhoea"); have("back pain"); have("abdominal pain"); have("nausea"); have("vomiting"); have("constipation"); have("new onset diabetes")}7, X>60.
consider("ultrasound") :- age(X), have("unexplained weight loss"), 1{have("diarrhoea"); have("back pain"); have("abdominal pain"); have("nausea"); have("vomiting"); have("constipation"); have("new onset diabetes")}7, X>60, not available("CT scan").
% 1.13
1 {offer("urgent investigation"); refer("suspected cancer pathway", cancer("pancreas"))} 1 :- 1{have("unexplained weight loss"); have("unexplained appetite loss")}2.
assess("additional symptoms") :- 1{have("unexplained appetite loss"); have("unexplained weight loss")}2.
% Background Knowledge
offered(P) :- offer(P).