export let populationVariables = {
  items: [
    {
      displayName: "Sex",
      id: "sex",
      splits: [
        {
          _checked: false,
          value: "male",
          valueDisplayName: "Male",
        },
        {
          _checked: false,
          value: "female",
          valueDisplayName: "Female",
        },
      ],
    },
    {
      displayName: "Age",
      id: "age",
      splits: [
        {
          _checked: false,
          value: "young",
          valueDisplayName: "<30 years old",
        },
        {
          _checked: false,
          value: "middle",
          valueDisplayName: "30-60 years old",
        },
        {
          _checked: false,
          value: "old",
          valueDisplayName: ">60 years old",
        },
      ],
    },
    {
      displayName: "Patient Location",
      id: "loc",
      splits: [
        {
          _checked: false,
          value: "inpat",
          valueDisplayName: "Inpatient",
        },
        {
          _checked: false,
          value: "outpat",
          valueDisplayName: "Outpatient",
        },
        {
          _checked: false,
          value: "ed",
          valueDisplayName: "Emergency room",
        },
        {
          _checked: false,
          value: "inst",
          valueDisplayName: "Institutional",
        },
      ],
    },
    {
      displayName: "BMI",
      id: "bmi",
      splits: [
        {
          _checked: false,
          value: "under",
          valueDisplayName: "Underweight",
        },
        {
          _checked: false,
          value: "healthy",
          valueDisplayName: "Healthy weight",
        },
        {
          _checked: false,
          value: "over",
          valueDisplayName: "Overweight",
        },
        {
          _checked: false,
          value: "obese",
          valueDisplayName: "Obese",
        },
      ],
    },
    {
      displayName: "Immune Status",
      id: "immuno",
      splits: [
        {
          _checked: false,
          value: "suppress",
          valueDisplayName: "Immunosuppressed",
        },
        {
          _checked: false,
          value: "competent",
          valueDisplayName: "Immunocompetent",
        },
      ],
    },
    {
      displayName: "Smoking Status",
      id: "smoke",
      splits: [
        {
          _checked: false,
          value: "current",
          valueDisplayName: "Current smokers",
        },
        {
          _checked: false,
          value: "former",
          valueDisplayName: "Former smokers",
        },
        {
          _checked: false,
          value: "never",
          valueDisplayName: "Never smoked",
        },
      ],
    },
    {
      displayName: "Neighborhood Income",
      id: "ses",
      splits: [
        {
          _checked: false,
          value: "1",
          valueDisplayName: "< $52,000",
        },
        {
          _checked: false,
          value: "2",
          valueDisplayName: "$52,000-$78,000",
        },
        {
          _checked: false,
          value: "3",
          valueDisplayName: "$78,000-$104,000",
        },
        {
          _checked: false,
          value: "4",
          valueDisplayName: "$104,000-$130,000",
        },
        {
          _checked: false,
          value: "5",
          valueDisplayName: ">$130,000",
        },
      ],
    },
    {
      displayName: "Race/Ethnicity",
      id: "eth",
      splits: [
        {
          _checked: false,
          value: "white",
          valueDisplayName: "White",
        },
        {
          _checked: false,
          value: "black",
          valueDisplayName: "Black",
        },
        {
          _checked: false,
          value: "asian",
          valueDisplayName: "Asian/Pacific islander",
        },
        {
          _checked: false,
          value: "hisp",
          valueDisplayName: "Hispanic",
        },
        {
          _checked: false,
          value: "other",
          valueDisplayName: "Unknown/Other",
        },
      ],
    },
    {
      displayName: "Pregnancy Status",
      id: "preg",
      splits: [
        {
          _checked: false,
          value: "pregnant",
          valueDisplayName: "Pregnant",
        },
        {
          _checked: false,
          value: "not",
          valueDisplayName: "Not pregnant",
        },
      ],
    },
    {
      displayName: "Heart Conditions",
      id: "HEART       ",
      splits: [
        {
          _checked: false,
          value: "true_HEART       ",
          valueDisplayName: "Known heart conditions",
        },
        {
          _checked: false,
          value: "false_HEART       ",
          valueDisplayName: "No reported heart conditions",
        },
      ],
    },
    {
      displayName: "Peripheral Vascular Disease",
      id: "PERIVASC    ",
      splits: [
        {
          _checked: false,
          value: "true_PERIVASC    ",
          valueDisplayName: "Known peripheral vascular disease",
        },
        {
          _checked: false,
          value: "false_PERIVASC    ",
          valueDisplayName: "No reported peripheral vascular disease",
        },
      ],
    },
    {
      displayName: "Cerebrovascular Disease",
      id: "CBVD        ",
      splits: [
        {
          _checked: false,
          value: "true_CBVD        ",
          valueDisplayName: "Known cerebrovascular disease",
        },
        {
          _checked: false,
          value: "false_CBVD        ",
          valueDisplayName: "No reported cerebrovascular disease",
        },
      ],
    },
    {
      displayName: "Neurological Disorders",
      id: "NEURO       ",
      splits: [
        {
          _checked: false,
          value: "true_NEURO       ",
          valueDisplayName: "Known neurological disorders",
        },
        {
          _checked: false,
          value: "false_NEURO       ",
          valueDisplayName: "No reported neurological disorders",
        },
      ],
    },
    {
      displayName: "Pulmonary Disease",
      id: "LUNG        ",
      splits: [
        {
          _checked: false,
          value: "true_LUNG        ",
          valueDisplayName: "Known pulmonary disease",
        },
        {
          _checked: false,
          value: "false_LUNG        ",
          valueDisplayName: "No reported pulmonary disease",
        },
      ],
    },
    {
      displayName: "Connective Tissue Disease",
      id: "Rheum       ",
      splits: [
        {
          _checked: false,
          value: "true_Rheum       ",
          valueDisplayName: "Known connective tissue disease",
        },
        {
          _checked: false,
          value: "false_Rheum       ",
          valueDisplayName: "No reported connective tissue disease",
        },
      ],
    },
    {
      displayName: "Peptic Ulcer",
      id: "ULCER       ",
      splits: [
        {
          _checked: false,
          value: "true_ULCER       ",
          valueDisplayName: "Known peptic ulcer",
        },
        {
          _checked: false,
          value: "false_ULCER       ",
          valueDisplayName: "No reported peptic ulcer",
        },
      ],
    },
    {
      displayName: "Liver Disease",
      id: "LIVER       ",
      splits: [
        {
          _checked: false,
          value: "true_LIVER       ",
          valueDisplayName: "Known liver disease",
        },
        {
          _checked: false,
          value: "false_LIVER       ",
          valueDisplayName: "No reported liver disease",
        },
      ],
    },
    {
      displayName: "Diabetes",
      id: "DIAB        ",
      splits: [
        {
          _checked: false,
          value: "true_DIAB        ",
          valueDisplayName: "Known diabetes",
        },
        {
          _checked: false,
          value: "false_DIAB        ",
          valueDisplayName: "No reported diabetes",
        },
      ],
    },
    {
      displayName: "Disabilities",
      id: "DISAB       ",
      splits: [
        {
          _checked: false,
          value: "true_DISAB       ",
          valueDisplayName: "Known disabilities",
        },
        {
          _checked: false,
          value: "false_DISAB       ",
          valueDisplayName: "No reported disabilities",
        },
      ],
    },
    {
      displayName: "Renal Disease",
      id: "RENLFL      ",
      splits: [
        {
          _checked: false,
          value: "true_RENLFL      ",
          valueDisplayName: "Known renal disease",
        },
        {
          _checked: false,
          value: "false_RENLFL      ",
          valueDisplayName: "No reported renal disease",
        },
      ],
    },
    {
      displayName: "Cancer",
      id: "CANCER      ",
      splits: [
        {
          _checked: false,
          value: "true_CANCER      ",
          valueDisplayName: "Known cancer",
        },
        {
          _checked: false,
          value: "false_CANCER      ",
          valueDisplayName: "No reported cancer",
        },
      ],
    },
    {
      displayName: "Acquired Immunodeficiency Syndrome",
      id: "AIDS        ",
      splits: [
        {
          _checked: false,
          value: "true_AIDS        ",
          valueDisplayName: "Known acquired immunodeficiency syndrome",
        },
        {
          _checked: false,
          value: "false_AIDS        ",
          valueDisplayName: "No reported acquired immunodeficiency syndrome",
        },
      ],
    },
    {
      displayName: "Substance Abuse",
      id: "SUBS        ",
      splits: [
        {
          _checked: false,
          value: "true_SUBS        ",
          valueDisplayName: "Known substance abuse",
        },
        {
          _checked: false,
          value: "false_SUBS        ",
          valueDisplayName: "No reported substance abuse",
        },
      ],
    },
    {
      displayName: "Mental Health Conditions",
      id: "MH          ",
      splits: [
        {
          _checked: false,
          value: "true_MH          ",
          valueDisplayName: "Known mental health conditions",
        },
        {
          _checked: false,
          value: "false_MH          ",
          valueDisplayName: "No reported mental health conditions",
        },
      ],
    },
    {
      displayName: "Sickle Cell & Thalassemia",
      id: "SICKLE      ",
      splits: [
        {
          _checked: false,
          value: "true_SICKLE      ",
          valueDisplayName: "Known sickle cell & thalassemia",
        },
        {
          _checked: false,
          value: "false_SICKLE      ",
          valueDisplayName: "No reported sickle cell & thalassemia",
        },
      ],
    },
    {
      displayName: "Transplanted Organ And Tissue Status",
      id: "TRANSPL     ",
      splits: [
        {
          _checked: false,
          value: "true_TRANSPL     ",
          valueDisplayName: "Known transplanted organ and tissue status",
        },
        {
          _checked: false,
          value: "false_TRANSPL     ",
          valueDisplayName: "No reported transplanted organ and tissue status",
        },
      ],
    },
  ],
  version: 1,
};
