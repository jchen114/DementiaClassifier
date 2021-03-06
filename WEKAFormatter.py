from random import shuffle
import Driver as dvr

ARFF_DIR = 'arff files/'
FEATURES_DIR = '/'


attribute_dict = {
    'int': 'numeric',
    'float': 'numeric',
    'long': 'numeric',
    'str': 'string'
}


# ------------------------
# Fill these in the corresponding key names you guys use
# ------------------------

fraser_feature_dict = {
    # POS FEATURES
    "RatioPronoun": "Pronoun:noun ratio",
    "NP->PRP": "NP->PRP",
    # "": "Frequency",
    "NumAdverbs": "Adverbs",
    "ADVP->RB": "ADVP->RB",
    "VP->VBG_PP": "VP->VBG_PP",
    "VP->IN_S": "VP->IN_S",
    "VP->AUX_ADJP": "VP->AUX_ADJP",
    "VP->AUX_VP": "VP->AUX_VP",
    "VP->VBG": "VP->VBG",
    "VP->AUX": "VP->AUX",
    "VP->VBD_NP": "VP->VBD_NP",
    "INTJ->UH": "INTJ->UH",
    "NP->DT_NN": "NP->DT_NN",
    "proportion_below_threshold_0.5": "Cosine cutoff: 0.5",
    "NumVerbs": "Verb Frequency",
    "NumNouns": "Nouns",
    "MeanWordLength": "Word Length",
    "HonoreStatistic": "Honore's statistic",
    "NumInflectedVerbs": "Inflected verbs",
    "avg_cos_dist": "Average cosine distance",
    "VPTypeRate": "VP rate",
    "PProportion": "PP proportion",
    "PPTypeRate": "PP rate",
    # InfoUnits
    "keywordIUObjectWindow":   "Key word: window",
    "binaryIUObjectWindow":    "Info unit: window",
    "keywordIUObjectSink":     "KEY WORD: sink",
    "binaryIUSubjectSink":     "Info unit: sink",
    "keywordIUObjectCookie":   "KEY WORD: cookie",
    "binaryIUObjectCookie":    "Info unit: cookie",
    "keywordIUObjectCurtains": "Key word: curtain",
    "binaryIUObjectCurtains":  "Info unit: curtain",
    "binaryIUSubjectGirl":     "Info unit: girl",
    "binaryIUObjectDishes":    "Info unit: dish",
    "keywordIUObjectStool":    "Key word: stool",
    "binaryIUObjectStool":     "Info unit: stool",
    "keywordIUSubjectWoman":   "Key word: mother",
    "binaryIUSubjectWoman":    "Info unit: woman",
    # PsychoLing
    "getFamiliarityScore":  "Familiarity",
    "getConcretenessScore": "Concreteness",
    "getImagabilityScore":  "Imagability",
    "getAoaScore":          "Age of acquisition",
    "getSUBTLWordScores":   "SUBTL Word score",
    "getLightVerbCount":    "Light Verb Count",

}

fraser_feature_dict_mix = {
    # POS FEATURES
    "RatioPronoun": "Pronoun:noun ratio",
    "NP->PRP": "NP->PRP",
    "NumAdverbs": "Adverbs",
    "ADVP->RB": "ADVP->RB",
    "VP->VBG_PP": "VP->VBG_PP",
    "VP->IN_S": "VP->IN_S",
    "VP->AUX_ADJP": "VP->AUX_ADJP",
    "VP->AUX_VP": "VP->AUX_VP",
    "VP->VBG": "VP->VBG",
    "VP->AUX": "VP->AUX",
    "VP->VBD_NP": "VP->VBD_NP",
    "INTJ->UH": "INTJ->UH",
    "NP->DT_NN": "NP->DT_NN",
    "proportion_below_threshold_0.5": "Cosine cutoff: 0.5",
    "NumVerbs": "Verb Frequency",
    "NumNouns": "Nouns",
    "MeanWordLength": "Word Length",
    "HonoreStatistic": "Honore's statistic",
    "NumInflectedVerbs": "Inflected verbs",
    "avg_cos_dist": "Average cosine distance",
    "VPTypeRate": "VP rate",
    "PProportion": "PP proportion",
    "PPTypeRate": "PP rate",

    # psycholing
    "getFamiliarityScore":  "Familiarity",
    "getConcretenessScore": "Concreteness",
    "getImagabilityScore":  "Imagability",
    "getAoaScore":          "Age of acquisition",
    "getSUBTLWordScores":   "SUBTL Word score",
    "getLightVerbCount":    "Light Verb Count",

}


def make_arff_file(file_name, samples):
    arff_file_name = ARFF_DIR + file_name + ".arff"

    arff_file = open(arff_file_name, 'w+')
    # Write the headers
    # Write the relation
    arff_file.write('@RELATION \"' + file_name + '\"\n\n')
    # Assuming that all samples will have the same features
    # Assuming that all sample features are iterated in the same order
    shuffle(samples) # Randomize samples
    data_unzipped = zip(*samples)
    samples = list(data_unzipped[0])
    labels = list(data_unzipped[1])
    label_order = []
    for k,v in samples[0].iteritems():
        attribute_str = '@ATTRIBUTE '
        key = str(k).strip().replace('\'', '')
        attribute_str += '\'' + key + '\''+ ' ' + get_attribute_from_variable(v)
        label_order.append(k)
        arff_file.write(attribute_str + '\n')
    arff_file.write('@ATTRIBUTE class {Control, Dementia} \n')
    # Begin writing the data
    arff_file.write('@DATA\n')
    for sample in range(0, len(samples)):
        data_str = ''
        for k in label_order:
            data_str += str(samples[sample][k]).strip() + ','
        data_str += labels[sample]
        arff_file.write(data_str + '\n')
    arff_file.close()


def get_attribute_from_variable(var):

    if is_number(var):
        return "numeric"
    else:
        return "str"


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


# ----------------- TRAINING STUFFS ----------------- #

def train_clinical_test_clinical(clinical_samples):
    # Use all the features
    file_name = "clinical_clinical_all"
    make_arff_file(file_name, clinical_samples)


def train_all_test_all(all_samples):
    # USE ALL THE FEATURES
    file_name = "all_all_all"
    make_arff_file(file_name, all_samples)


def train_clinical_test_clinical_fraser_features(clinical_samples):
    # Use features found in fraser
    file_name = "clinical_clinical_fraser"
    # Comb the features in clinical_samples to match the ones in fraser
    unzipped_data = zip(*clinical_samples)
    samples = list(unzipped_data[0])
    labels = list(unzipped_data[1])
    fraser_samples = []
    for sample in samples:
        features = {}
        for k,v in sample.iteritems():
            if k in fraser_feature_dict.keys():
                features[fraser_feature_dict[k]] = v
        fraser_samples.append(features)
    samples = zip(fraser_samples, labels)
    make_arff_file(file_name, samples)


# def train_all_test_all_fraser_mix(all_samples):
#     file_name = "all_all_fraser_mix"
#     # Comb the features in clinical_samples to match the ones in fraser
#     unzipped_data = zip(*clinical_samples)
#     samples = list(unzipped_data[0])
#     labels = list(unzipped_data[1])
#     fraser_samples = []
#     for sample in samples:
#         features = {}
#         for k, v in sample.iteritems():
#             if k in fraser_feature_dict_mix.keys():
#                 features[fraser_feature_dict_mix[k]] = v
#         fraser_samples.append(features)
#     samples = zip(fraser_samples, labels)
#     make_arff_file(file_name, samples)



if __name__ == "__main__":

    op = dvr.get_optima_feature_data()
    db = dvr.get_dementiabank_feature_data()

    make_arff_file("optima_all_features",op)
    make_arff_file("dbank_all_features",db)

    # # Load clinical data sets.
    # clinical_samples = dvr.get_clinical_feature_data()

    # # Train on clinical and test on clinical with all features
    # train_clinical_test_clinical(clinical_samples)

    # # Train on clinical and test on clinical with fraser features
    # train_clinical_test_clinical_fraser_features(clinical_samples)

    # # Load the clinical and non-clinical data sets
    # all_samples = dvr.get_all_feature_data()

    # # Train on all and test on all with all features
    # train_all_test_all(all_samples)

    # # Train on all and test on all with mix of fraser features
    # train_all_test_all_fraser_mix(all_samples)



