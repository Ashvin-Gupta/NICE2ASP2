% 1.1.1
offer("pancreatic_protocol_ct") :- suspected(cancer("pancreas")), have("obstructive_jaundice").
offer("draining_bile_duct") :- offered("pancreatic_protocol_ct"), suspected(cancer("pancreas")), have("obstructive_jaundice").
% 1.1.2                          
1 {offer("FDG-PET/CT"); offer("EUS_with_tissue")} 2 :- findings_from_procedure("pancreatic_protocol_ct", "unclear_diagnosis"), offered("pancreatic_protocol_ct"), have("obstructive_jaundice").
% 1.1.3
offer("biliary_brushing") :- findings_from_procedure("EUS_with_tissue", "no_tissue_diagnosis"), offer("ERCP", "bilary_obstruction"), have("obstructive_jaundice").
% 1.1.4
offer("pancreatic_protocol_ct") :- have("pancreatic_abnormalities"), not have("jaundice").
% 1.1.5
1 {offer("FDG-PET/CT"); offer("EUS_with_tissue")} 2 :- findings_from_procedure("pancreatic_protocol_ct", "unclear_diagnosis"), offered("pancreatic_protocol_ct"), have("pancreatic_abnormalities"), not have("jaundice").
% 1.1.6
offer("EUS_with_tissue") :- 1{need("cytological_samples"); need("histological_samples")}2, have("pancreatic_abnormalities"), not have("jaundice").
% 1.1.7
1{ offer("pancreatic_protocol_ct"); offer("MRI/MRCP")} 1 :- have("pancreatic_cysts").
offer("pancreatic_protocol_ct") :- offered("MRI/MRCP"), need("more_information"), have("pancreatic_cysts").
offer("MRI/MRCP") :- offered("pancreatic_protocol_ct"), need("more_information"), have("pancreatic_cysts").
% 1.1.8
refer("resection") :- have("obstructive_jaundice"), findings("cystic_lesions", "head_of_pancreas"), have("pancreatic_cysts").
refer("resection") :- findings("solid_component", "pancreatic_cyst"), have("pancreatic_cysts").
refer("resection") :- findings("10mm", "pancreatic_duct"), have("pancreatic_cysts").
% 1.1.9
offer("EUS") :- offered("pancreatic_protocol_ct"), offered("MRI/MRCP"), 1{need("maligancy_likelihood"); need("info_on_surgery")}2, have("pancreatic_cysts").
% 1.1.10
consider("fine-needle", "EUS") :- need("maligancy_likelihood"), have("pancreatic_cysts"), offered("EUS").
% 1.1.11
1{offer("CEA_assay"); offer("cytology")} 1 :- offered("fine_needle"), sufficient_sample, have("pancreatic_cysts").
% 1.1.12
follow("staging_recommendations") :- findings("malignancy", "pancreatic_cysts"), have("pancreatic_cysts").
% 1.1.13  
ask("family_history") :- have(cancer("pancreas")).
address("inherited_risk_concerns") :- have(cancer("pancreas")), first_degree_relative(cancer("pancreas"), _).
% 1.1.14
offer("surveillance", cancer("pancreas")) :- have("hereditary_pancreatitis"), have("PRSS1"), have("inherited_high_risk").
offer("surveillance", cancer("pancreas")) :- 1{have("BRCA1");have("BRCA2");have("PALB2");have("CDKN2A")}4, first_degree_relative(cancer("pancreas"),_), have("inherited_high_risk").
offer("surveillance", cancer("pancreas")) :- have("peutz_jeghers"), have("inherited_high_risk").
% 1.1.15
consider("surveillance", cancer("pancreas")) :- have("lynch_syndrome"), first_degree_relative(cancer("pancreas"),_), have("inherited_high_risk").
consider("surveillance", cancer("pancreas")) :- first_degree_relative(cancer("pancreas"),X), first_degree_relative(cancer("pancreas"),Y), X!=Y, have("inherited_high_risk").
% 1.1.16
1{ consider("MRI/MRCP"); consider("EUS")} 1 :-  not have("hereditary_pancreatitis"), offer("surveillance", cancer("pancreas")), have("inherited_high_risk").
% 1.1.17
consider("pancreatic_protocol_ct") :- have("hereditary_pancreatitis"), have("PRSS1"), offer("surveillance", cancer("pancreas")), have("inherited_high_risk").
% 1.1.18
:- offer("EUS"), have("hereditary_pancreatitis"), have("inherited_high_risk").
% 1.3.1
3{offer("pancreatic_protocol_ct", "chest"); offer("pancreatic_protocol_ct", "abdomen"); offer("pancreatic_protocol_ct", "pelvis")} 3 :- have(cancer("pancreas")), not offered("pancreatic_protocol_ct").
% 1.3.2
offer("FDG-PET/CT") :- 1{treatment("surgery"); treatment("radiotherapy"); treatment("systemic_therapy")}3, findings_from_procedure("pancreatic_protocol_ct", "localised_disease"). 
% 1.3.3
consider("MRI/MRCP") :-  need("more_information"), suspected("liver_metastases").
consider("endoscopic_ultrasound") :-  need("more_information"), need("tumor_staging"), need("node_staging").
consider("lacroscpoic_ultrasound") :- suspected("small_volume_peritoneal"), susptected("liver_metastases"), possible("resectional_surgery").
% 1.2.4
refer("suspected_cancer_pathway", cancer("pancreas")) :- age(X), have("jaundice"), X>=40.
% 1.2.5
consider("CT_scan") :- age(X), have("unexplained_weight_loss"), 1{have("diarrhoea"); have("back_pain"); have("abdominal_pain"); have("nausea"); have("vomiting"); have("constipation"); have("new_onset_diabetes")}7, X>60.
consider("ultrasound") :- age(X), have("unexplained_weight_loss"), 1{have("diarrhoea"); have("back_pain"); have("abdominal_pain"); have("nausea"); have("vomiting"); have("constipation"); have("new_onset_diabetes")}7, X>60, not available("CT_scan").
% 1.13
1 {offer("urgent_investigation"); refer("suspected_cancer_pathway", cancer("pancreas"))} 1 :- 1{have("unexplained_weight_loss"); have("unexplained_appetite_loss")}2.
assess("additional_symptoms") :- 1{have("unexplained_appetite_loss"); have("unexplained_weight_loss")}2.
% Background Knowledge
offered(P) :- offer(P).