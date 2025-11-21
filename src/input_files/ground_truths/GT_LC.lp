% [1.3.1]
% Only use sputum cytology for investigation in people with suspected lung cancer
% who have centrally placed nodules or masses and who decline or cannot tolerate
% bronchoscopy or other invasive tests
offer("sputum_cytology") :- suspected(cancer("lung")), 1{have("centrally_placed_nodules"); have("centrally_placed_masses")}2, decline("bronchoscopy"), decline("invasive_tests").
offer("sputum_cytology") :- suspected(cancer("lung")), 1{have("centrally_placed_nodules"); have("centrally_placed_masses")}2, not tolerate("bronchoscopy"), not tolerate("invasive_tests").

% [1.3.2]
% Offer people with known or suspected lung cancer a contrast-enhanced chest CT
% scan to further the diagnosis and stage the disease. Include the liver, adrenals
% and lower neck in the scan. The guideline committee also recognised that
% contrast medium should only be given with caution to people with known renal
% impairment.
offer("contrast_enhanced_chest_CT_scan") :- 1{have(cancer("lung")); suspected(cancer("lung"))}2.
3{include("contrast_enhanced_chest_CT_scan", "liver"); include("contrast_enhanced_chest_CT_scan", "adrenals"); include("contrast_enhanced_chest_CT_scan", "lower_neck")} 3 :- offer("contrast_enhanced_chest_CT_scan").

% 1.3.3
% When assessing mediastinal and chest wall invasion:
% • be aware that CT alone may not be reliable
% • consider other techniques such as ultrasound if there is doubt
% • be aware that surgical assessment may be necessary if there are no
% contraindications to resection.
aware("CT", "alone_unreliable") :- have("chest_wall_invasion"), offered("contrast_enhanced_chest_CT_scan").
consider("ultrasound") :- have("chest_wall_invasion"), offered("contrast_enhanced_chest_CT_scan"), findings_from_procedure("contrast_enhanced_chest_CT_scan", "unclear_diagnosis").


% [1.3.4]
% Ensure that all people with lung cancer who could potentially have treatment with
% curative intent are offered positron-emission tomography CT (PET-CT) before
% treatment
offer("PET-CT") :- have(cancer("lung")), offered("treatment_with_curative_intent").

% 1.3.5
% Every cancer alliance should have a system of rapid access to PET-CT scanning
% for eligible people


% [1.3.6]
% Do not routinely use MRI to assess the stage of the primary tumour (T-stage) in
% non-small-cell lung cancer (NSCLC)
:- have("NSCLC"), offer("MRI"), assess_stage("primary_tumour").

% [1.3.7]
% Use MRI when necessary to assess the extent of disease, for people with superior sulcus tumours
offer("MRI") :- have("superior_sulcus_tumours").

% [1.3.8]
% Offer endobronchial ultrasound-guided transbronchial needle aspiration (EBUSTBNA) for biopsy of paratracheal and peri-bronchial intra-parenchymal lung
% lesions.
offer("EBUS-TBNA") :- biopsy("paratracheal_lesions").
offer("EBUS-TBNA") :- biopsy("peri-bronchial_intra-parenchymal_lung_lesions").

% 1.3.9
% Every cancer alliance should have at least 1 centre with EBUS and/or endoscopic
% ultrasound (EUS) to ensure timely access.

% 1.3.10
% Audit the local test performance of EBUS-TBNA and endoscopic ultrasoundguided fine-needle aspiration (EUS-FNA)

% 1.3.11
% When taking samples, ensure they are adequate (without unacceptable risk to
% the person) to permit pathological diagnosis, including tumour subtyping and
% assessment of predictive markers.

% 1.3.12
% For guidance on EGFR-TK mutation testing, see the NICE diagnostics guidance
% on EGFR-TK mutation testing in adults with locally advanced or metastatic nonsmall-cell lung cancer.

clarify("EGFR-TK_mutation_testing") :- have("NSCLC").

% 1.3.13
% Choose investigations that give the most information about diagnosis and staging
% with the least risk to the person. Think carefully before performing a test that
% gives only diagnostic pathology when information on staging is also needed to
% guide treatment.


% [1.3.14]
% Perform contrast-enhanced CT of the chest, liver adrenals and lower neck before
% any biopsy procedure.
offer("contrast_enhanced_chest_CT_scan") :- not perform("biopsy_procedure"), suspect(cancer("lung")).
3{include("contrast_enhanced_chest_CT_scan", "liver"); include("contrast_enhanced_chest_CT_scan", "adrenals"); include("contrast_enhanced_chest_CT_scan", "lower_neck")} 3 :- offer("contrast_enhanced_chest_CT_scan").

% [1.3.15]
% Offer image-guided biopsy to people with peripheral lung lesions when treatment
% can be planned on the basis of this test
offer("image-guided_biopsy") :- have("peripheral_lung_lesions"), plan_treatment("image-guided_biopsy").

% 1.3.16
% Biopsy any enlarged intrathoracic nodes (10 mm or larger maximum short axis on
% CT) or other lesions in preference to the primary lesion if determination of nodal
% stage affects treatment. Some people with lung cancer will not be well enough for
% treatment with curative intent. This needs to be taken into account when
% choosing diagnostic and staging investigations.
biopsy("enlarged_intrathoracic_nodes") :- size("intrathoracic_nodes", X), X >= 10, influence("nodal_staging", "treatment").
biopsy("other_lesions") :- influence("nodal_staging", "treatment").

% [1.3.17]
% Offer flexible bronchoscopy to people with central lesions on CT if nodal staging
% does not influence treatment.
offer("flexible_bronchoscopy") :- findings_from_procedure("CT", "central_lesions"), not influence("nodal_staging", "treatment").

% [1.3.18]
% Offer PET-CT as the preferred first test after CT with a low probability of nodal
% malignancy (lymph nodes below 10 mm maximum short axis on CT), for people
% with lung cancer who could potentially have treatment with curative intent. 
offer("PET-CT") :- have(cancer("lung")), offered("treatment_with_curative_intent"), findings_from_procedure("CT", "lymph_nodes_below_10mm").

% [1.3.19]
% Offer PET-CT (if not already done), followed by EBUS-TBNA and/or EUS-FNA, to
% people with suspected lung cancer who have enlarged intrathoracic lymph nodes
% (lymph nodes greater than or equal to 10 mm short axis on CT) and who could
% potentially have treatment with curative intent.
offer("PET-CT") :- suspected(cancer("lung")), offered("treatment_with_curative_intent"), findings_from_procedure("CT", "lymph_nodes_greater_than_or_equal_to_10mm").
1{offer("EBUS-TBNA"); offer("EUS-FNA")} 2 :- suspected(cancer("lung")), offered("treatment_with_curative_intent"), findings_from_procedure("CT", "lymph_nodes_greater_than_or_equal_to_10mm"), offered("PET-CT").

% [1.3.20]
% Evaluate PET-CT-positive or enlarged intrathoracic nodes using a systematic
% approach (sampling any suspicious node on CT, PET or USS) with EBUS-TBNA
% and/or EUS-FNA if nodal status would affect the treatment plan.
1 {offer("EBUS-TBNA"); offer("EUS-FNA")} 2 :- findings_from_procedure("PET-CT", "positive"), influence("nodal_status", "treatment").
1 {offer("EBUS-TBNA"); offer("EUS-FNA")} 2 :- have("intrathoracic_nodes"), influence("nodal_status", "treatment").

% 1.3.1
% Consider surgical mediastinal staging for people with a negative EBUS-TBNA or
% EUS-FNA if clinical suspicion of nodal malignancy is high and nodal status would
% affect their treatment plan.

consider("surgical_mediastinal_staging") :- 1{findings_from_procedure("EBUS-TBNA", "negative"); findings_from_procedure("EUS-FNA", "negative")}2, suspected("nodal_malignancy"), influence("nodal_staging", "treatment").

% 1.3.22
% Confirm the presence of isolated distant metastases/synchronous tumours by
% biopsy or further imaging (for example, MRI or PET-CT) in people being
% considered for treatment with curative intent.
1{offer("biopsy");offer("MRI"); offer("PET-CT")} 3 :- offered("treatment_with_curative_intent"), suspected("isolated_distant_metastases").

% [1.3.23]
% Do not offer dedicated brain imaging to people with clinical stage I NSCLC who
% have no neurological symptoms and are having treatment with curative intent.
:- have("NSCLC", "clinical_stage_I"), not have("neurological_symptoms"), offered("treatment_with_curative_intent"), offer("brain_imaging").

% [1.3.24]
% Offer contrast-enhanced brain CT to people with clinical stage II NSCLC who are
% having treatment with curative intent. If CT shows suspected brain metastases,
% offer contrast-enhanced brain MRI.
offer("contrast_enhanced_brain_CT") :- have("NSCLC", "clinical_stage_II"), offered("treatment_with_curative_intent").
offer("contrast_enhanced_brain_MRI") :- have("NSCLC", "clinical_stage_II"), offered("treatment_with_curative_intent"), findings_from_procedure("contrast_enhanced_brain_CT", "suspected_brain_metastases").

% [1.3.25]
% Offer contrast-enhanced brain MRI for people with stage III NSCLC who are
% having treatment with curative intent.
offer("contrast_enhanced_brain_MRI") :- have("NSCLC", "stage_III"), offered("treatment_with_curative_intent").

% [1.3.26]
% Offer people with clinical features suggestive of intracranial pathology CT of the
% head followed by MRI if normal, or MRI as an initial test.
offer("CT") :- suspected("intracranial_pathology").
offer("MRI") :- suspected("intracranial_pathology"), findings_from_procedure("CT", "normal").

% [1.3.27]
% Perform an X-ray as the first test for people with localised signs or symptoms of
% bone metastasis. If the results are negative or inconclusive, offer bone
% scintigraphy or an MRI scan. 
offer("X-ray") :- have("bone_metastasis").
offer("bone_scintigraphy") :- have("bone_metastasis"), 1{findings_from_procedure("X-ray", "negative"); findings_from_procedure("X-ray", "inconclusive")}2.
offer("MRI") :- have("bone_metastasis"), 1{findings_from_procedure("X-ray", "negative"); findings_from_procedure("X-ray", "inconclusive")}2.
% [1.3.28]
% Avoid bone scintigraphy when PET-CT has not shown bone metastases
:- offer("bone_scintigraphy"), not findings_from_procedure("PET-CT", "bone_metastases").

% 1.3.29
% Provide treatment without undue delay for people who have lung cancer that is
% suitable for radical treatment or chemotherapy, or who need radiotherapy or
% ablative treatment for relief of symptoms. 
provide("urgent_treatment") :- have(cancer("lung")), offered("treatment_with_curative_intent"), 1{need("radical_treatment"); need("chemotherapy"); need("radiotherapy")}3.

% [1.3.30]
% Refer all people with a suspected diagnosis of lung cancer to a member of a lung
% cancer multidisciplinary team (usually a chest physician).
refer("lung_cancer_multidisciplinary_team", cancer("lung")) :- suspect(cancer("lung")).

% 1.3.1
% The care of all people with a working diagnosis of lung cancer should be
% discussed at a lung cancer multidisciplinary team meeting.

% [1.1.1]
refer("suspected_cancer_pathway_referral", cancer("lung")) :- findings("chest_X-ray", "suggest_lung_cancer").
refer("suspected_cancer_pathway_referral", cancer("lung")) :- age(X), X>=40, have("haemoptysis").

% [1.1.2]
offer("chest_X-ray") :- age(X), X>=40, 2{have("cough"); have("fatigue"); have("shortness_of_breath"); have("chest_pain"); have("weight_loss"); have("appetite_loss")}6.
offer("chest_X_ray") :- age(X), X>=40, have("smoked"), 1{have("cough"); have("fatigue"); have("shortness_of_breath"); have("chest_pain"); have("weight_loss"); have("appetite_loss")}6.

% [1.1.3]
consider("chest_X-ray") :- age(X), X>=40, 1{have("persistent_or_recurrent_chest_infection"); have("finger_clubbing"); have("supraclavicular_lymphadenopathy"); have("persistent_cervical_lymphadenopathy"); have("chest_signs")}5.


offered(X) :- offer(X).