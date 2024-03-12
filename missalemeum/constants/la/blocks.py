import itertools

from constants import common as constants

POST_EPIPHANY = (
    (constants.TEMPORA_EPI1_0,),
    (constants.TEMPORA_EPI1_1,),
    (constants.TEMPORA_EPI1_2,),
    (constants.TEMPORA_EPI1_3,),
    (constants.TEMPORA_EPI1_4,),
    (constants.TEMPORA_EPI1_5,),
    (constants.TEMPORA_EPI1_6,),
    (constants.TEMPORA_EPI2_0,),
    (constants.TEMPORA_EPI2_1,),
    (constants.TEMPORA_EPI2_2,),
    (constants.TEMPORA_EPI2_3,),
    (constants.TEMPORA_EPI2_4,),
    (constants.TEMPORA_EPI2_5,),
    (constants.TEMPORA_EPI2_6,),
    (constants.TEMPORA_EPI3_0,),
    (constants.TEMPORA_EPI3_1,),
    (constants.TEMPORA_EPI3_2,),
    (constants.TEMPORA_EPI3_3,),
    (constants.TEMPORA_EPI3_4,),
    (constants.TEMPORA_EPI3_5,),
    (constants.TEMPORA_EPI3_6,),
    (constants.TEMPORA_EPI4_0,),
    (constants.TEMPORA_EPI4_1,),
    (constants.TEMPORA_EPI4_2,),
    (constants.TEMPORA_EPI4_3,),
    (constants.TEMPORA_EPI4_4,),
    (constants.TEMPORA_EPI4_5,),
    (constants.TEMPORA_EPI4_6,),
    (constants.TEMPORA_EPI5_0,),
    (constants.TEMPORA_EPI5_1,),
    (constants.TEMPORA_EPI5_2,),
    (constants.TEMPORA_EPI5_3,),
    (constants.TEMPORA_EPI5_4,),
    (constants.TEMPORA_EPI5_5,),
    (constants.TEMPORA_EPI5_6,),
    (constants.TEMPORA_EPI6_0,),
    (constants.TEMPORA_EPI6_1,),
    (constants.TEMPORA_EPI6_2,),
    (constants.TEMPORA_EPI6_3,),
    (constants.TEMPORA_EPI6_4,),
    (constants.TEMPORA_EPI6_5,),
    (constants.TEMPORA_EPI6_6,),
)

FROM_PRE_LENT_TO_POST_PENTECOST = (
    (constants.TEMPORA_QUADP1_0,),
    (constants.TEMPORA_QUADP1_1,),
    (constants.TEMPORA_QUADP1_2,),
    (constants.TEMPORA_QUADP1_3,),
    (constants.TEMPORA_QUADP1_4,),
    (constants.TEMPORA_QUADP1_5,),
    (constants.TEMPORA_QUADP1_6,),
    (constants.TEMPORA_QUADP2_0,),
    (constants.TEMPORA_QUADP2_1,),
    (constants.TEMPORA_QUADP2_2,),
    (constants.TEMPORA_QUADP2_3,),
    (constants.TEMPORA_QUADP2_4,),
    (constants.TEMPORA_QUADP2_5,),
    (constants.TEMPORA_QUADP2_6,),
    (constants.TEMPORA_QUADP3_0,),
    (constants.TEMPORA_QUADP3_1,),
    (constants.TEMPORA_QUADP3_2,),
    (constants.TEMPORA_QUADP3_3,),
    (constants.TEMPORA_QUADP3_4,),
    (constants.TEMPORA_QUADP3_5,),
    (constants.TEMPORA_QUADP3_6,),
    (constants.TEMPORA_QUAD1_0,),
    (constants.TEMPORA_QUAD1_1,),
    (constants.TEMPORA_QUAD1_2,),
    (constants.TEMPORA_QUAD1_3,),
    (constants.TEMPORA_QUAD1_4,),
    (constants.TEMPORA_QUAD1_5,),
    (constants.TEMPORA_QUAD1_6,),
    (constants.TEMPORA_QUAD2_0,),
    (constants.TEMPORA_QUAD2_1,),
    (constants.TEMPORA_QUAD2_2,),
    (constants.TEMPORA_QUAD2_3,),
    (constants.TEMPORA_QUAD2_4,),
    (constants.TEMPORA_QUAD2_5,),
    (constants.TEMPORA_QUAD2_6,),
    (constants.TEMPORA_QUAD3_0,),
    (constants.TEMPORA_QUAD3_1,),
    (constants.TEMPORA_QUAD3_2,),
    (constants.TEMPORA_QUAD3_3,),
    (constants.TEMPORA_QUAD3_4,),
    (constants.TEMPORA_QUAD3_5,),
    (constants.TEMPORA_QUAD3_6,),
    (constants.TEMPORA_QUAD4_0,),
    (constants.TEMPORA_QUAD4_1,),
    (constants.TEMPORA_QUAD4_2,),
    (constants.TEMPORA_QUAD4_3,),
    (constants.TEMPORA_QUAD4_4,),
    (constants.TEMPORA_QUAD4_5,),
    (constants.TEMPORA_QUAD4_6,),
    (constants.TEMPORA_QUAD5_0,),
    (constants.TEMPORA_QUAD5_1,),
    (constants.TEMPORA_QUAD5_2,),
    (constants.TEMPORA_QUAD5_3,),
    (constants.TEMPORA_QUAD5_4,),
    (constants.TEMPORA_QUAD5_5, constants.TEMPORA_QUAD5_5C),
    (constants.TEMPORA_QUAD5_6,),
    (constants.TEMPORA_QUAD6_0,),
    (constants.TEMPORA_QUAD6_1,),
    (constants.TEMPORA_QUAD6_2,),
    (constants.TEMPORA_QUAD6_3,),
    (constants.TEMPORA_QUAD6_4,),
    (constants.TEMPORA_QUAD6_5,),
    (constants.TEMPORA_QUAD6_6,),
    (constants.TEMPORA_PASC0_0,),
    (constants.TEMPORA_PASC0_1,),
    (constants.TEMPORA_PASC0_2,),
    (constants.TEMPORA_PASC0_3,),
    (constants.TEMPORA_PASC0_4,),
    (constants.TEMPORA_PASC0_5,),
    (constants.TEMPORA_PASC0_6,),
    (constants.TEMPORA_PASC1_0,),
    (constants.TEMPORA_PASC1_1,),
    (constants.TEMPORA_PASC1_2,),
    (constants.TEMPORA_PASC1_3,),
    (constants.TEMPORA_PASC1_4,),
    (constants.TEMPORA_PASC1_5,),
    (constants.TEMPORA_PASC1_6,),
    (constants.TEMPORA_PASC2_0,),
    (constants.TEMPORA_PASC2_1,),
    (constants.TEMPORA_PASC2_2,),
    (constants.TEMPORA_PASC2_3,),
    (constants.TEMPORA_PASC2_4,),
    (constants.TEMPORA_PASC2_5,),
    (constants.TEMPORA_PASC2_6,),
    (constants.TEMPORA_PASC3_0,),
    (constants.TEMPORA_PASC3_1,),
    (constants.TEMPORA_PASC3_2,),
    (constants.TEMPORA_PASC3_3,),
    (constants.TEMPORA_PASC3_4,),
    (constants.TEMPORA_PASC3_5,),
    (constants.TEMPORA_PASC3_6,),
    (constants.TEMPORA_PASC4_0,),
    (constants.TEMPORA_PASC4_1,),
    (constants.TEMPORA_PASC4_2,),
    (constants.TEMPORA_PASC4_3,),
    (constants.TEMPORA_PASC4_4,),
    (constants.TEMPORA_PASC4_5,),
    (constants.TEMPORA_PASC4_6,),
    (constants.TEMPORA_PASC5_0,),
    (constants.TEMPORA_PASC5_1,),
    (constants.TEMPORA_PASC5_2,),
    (constants.TEMPORA_PASC5_3,),
    (constants.TEMPORA_PASC5_4,),
    (constants.TEMPORA_PASC5_5,),
    (constants.TEMPORA_PASC5_6,),
    (constants.TEMPORA_PASC6_0,),
    (constants.TEMPORA_PASC6_1,),
    (constants.TEMPORA_PASC6_2,),
    (constants.TEMPORA_PASC6_3,),
    (constants.TEMPORA_PASC6_4,),
    (constants.TEMPORA_PASC6_5,),
    (constants.TEMPORA_PASC6_6,),
    (constants.TEMPORA_PASC7_0,),
    (constants.TEMPORA_PASC7_1,),
    (constants.TEMPORA_PASC7_2,),
    (constants.TEMPORA_PASC7_3,),
    (constants.TEMPORA_PASC7_4,),
    (constants.TEMPORA_PASC7_5,),
    (constants.TEMPORA_PASC7_6,),
    (constants.TEMPORA_PENT01_0,),
    (constants.TEMPORA_PENT01_1,),
    (constants.TEMPORA_PENT01_2,),
    (constants.TEMPORA_PENT01_3,),
    (constants.TEMPORA_PENT01_4,),
    (constants.TEMPORA_PENT01_5,),
    (constants.TEMPORA_PENT01_6,),
    (constants.TEMPORA_PENT02_0,),
    (constants.TEMPORA_PENT02_1,),
    (constants.TEMPORA_PENT02_2,),
    (constants.TEMPORA_PENT02_3,),
    (constants.TEMPORA_PENT02_4,),
    (constants.TEMPORA_PENT02_5,),
    (constants.TEMPORA_PENT02_6,),
    (constants.TEMPORA_PENT03_0,),
    (constants.TEMPORA_PENT03_1,),
    (constants.TEMPORA_PENT03_2,),
    (constants.TEMPORA_PENT03_3,),
    (constants.TEMPORA_PENT03_4,),
    (constants.TEMPORA_PENT03_5,),
    (constants.TEMPORA_PENT03_6,),
    (constants.TEMPORA_PENT04_0,),
    (constants.TEMPORA_PENT04_1,),
    (constants.TEMPORA_PENT04_2,),
    (constants.TEMPORA_PENT04_3,),
    (constants.TEMPORA_PENT04_4,),
    (constants.TEMPORA_PENT04_5,),
    (constants.TEMPORA_PENT04_6,),
    (constants.TEMPORA_PENT05_0,),
    (constants.TEMPORA_PENT05_1,),
    (constants.TEMPORA_PENT05_2,),
    (constants.TEMPORA_PENT05_3,),
    (constants.TEMPORA_PENT05_4,),
    (constants.TEMPORA_PENT05_5,),
    (constants.TEMPORA_PENT05_6,),
    (constants.TEMPORA_PENT06_0,),
    (constants.TEMPORA_PENT06_1,),
    (constants.TEMPORA_PENT06_2,),
    (constants.TEMPORA_PENT06_3,),
    (constants.TEMPORA_PENT06_4,),
    (constants.TEMPORA_PENT06_5,),
    (constants.TEMPORA_PENT06_6,),
    (constants.TEMPORA_PENT07_0,),
    (constants.TEMPORA_PENT07_1,),
    (constants.TEMPORA_PENT07_2,),
    (constants.TEMPORA_PENT07_3,),
    (constants.TEMPORA_PENT07_4,),
    (constants.TEMPORA_PENT07_5,),
    (constants.TEMPORA_PENT07_6,),
    (constants.TEMPORA_PENT08_0,),
    (constants.TEMPORA_PENT08_1,),
    (constants.TEMPORA_PENT08_2,),
    (constants.TEMPORA_PENT08_3,),
    (constants.TEMPORA_PENT08_4,),
    (constants.TEMPORA_PENT08_5,),
    (constants.TEMPORA_PENT08_6,),
    (constants.TEMPORA_PENT09_0,),
    (constants.TEMPORA_PENT09_1,),
    (constants.TEMPORA_PENT09_2,),
    (constants.TEMPORA_PENT09_3,),
    (constants.TEMPORA_PENT09_4,),
    (constants.TEMPORA_PENT09_5,),
    (constants.TEMPORA_PENT09_6,),
    (constants.TEMPORA_PENT10_0,),
    (constants.TEMPORA_PENT10_1,),
    (constants.TEMPORA_PENT10_2,),
    (constants.TEMPORA_PENT10_3,),
    (constants.TEMPORA_PENT10_4,),
    (constants.TEMPORA_PENT10_5,),
    (constants.TEMPORA_PENT10_6,),
    (constants.TEMPORA_PENT11_0,),
    (constants.TEMPORA_PENT11_1,),
    (constants.TEMPORA_PENT11_2,),
    (constants.TEMPORA_PENT11_3,),
    (constants.TEMPORA_PENT11_4,),
    (constants.TEMPORA_PENT11_5,),
    (constants.TEMPORA_PENT11_6,),
    (constants.TEMPORA_PENT12_0,),
    (constants.TEMPORA_PENT12_1,),
    (constants.TEMPORA_PENT12_2,),
    (constants.TEMPORA_PENT12_3,),
    (constants.TEMPORA_PENT12_4,),
    (constants.TEMPORA_PENT12_5,),
    (constants.TEMPORA_PENT12_6,),
    (constants.TEMPORA_PENT13_0,),
    (constants.TEMPORA_PENT13_1,),
    (constants.TEMPORA_PENT13_2,),
    (constants.TEMPORA_PENT13_3,),
    (constants.TEMPORA_PENT13_4,),
    (constants.TEMPORA_PENT13_5,),
    (constants.TEMPORA_PENT13_6,),
    (constants.TEMPORA_PENT14_0,),
    (constants.TEMPORA_PENT14_1,),
    (constants.TEMPORA_PENT14_2,),
    (constants.TEMPORA_PENT14_3,),
    (constants.TEMPORA_PENT14_4,),
    (constants.TEMPORA_PENT14_5,),
    (constants.TEMPORA_PENT14_6,),
    (constants.TEMPORA_PENT15_0,),
    (constants.TEMPORA_PENT15_1,),
    (constants.TEMPORA_PENT15_2,),
    (constants.TEMPORA_PENT15_3,),
    (constants.TEMPORA_PENT15_4,),
    (constants.TEMPORA_PENT15_5,),
    (constants.TEMPORA_PENT15_6,),
    (constants.TEMPORA_PENT16_0,),
    (constants.TEMPORA_PENT16_1,),
    (constants.TEMPORA_PENT16_2,),
    (constants.TEMPORA_PENT16_3,),
    (constants.TEMPORA_PENT16_4,),
    (constants.TEMPORA_PENT16_5,),
    (constants.TEMPORA_PENT16_6,),
    (constants.TEMPORA_PENT17_0,),
    (constants.TEMPORA_PENT17_1,),
    (constants.TEMPORA_PENT17_2,),
    (constants.TEMPORA_PENT17_3,),
    (constants.TEMPORA_PENT17_4,),
    (constants.TEMPORA_PENT17_5,),
    (constants.TEMPORA_PENT17_6,),
    (constants.TEMPORA_PENT18_0,),
    (constants.TEMPORA_PENT18_1,),
    (constants.TEMPORA_PENT18_2,),
    (constants.TEMPORA_PENT18_3,),
    (constants.TEMPORA_PENT18_4,),
    (constants.TEMPORA_PENT18_5,),
    (constants.TEMPORA_PENT18_6,),
    (constants.TEMPORA_PENT19_0,),
    (constants.TEMPORA_PENT19_1,),
    (constants.TEMPORA_PENT19_2,),
    (constants.TEMPORA_PENT19_3,),
    (constants.TEMPORA_PENT19_4,),
    (constants.TEMPORA_PENT19_5,),
    (constants.TEMPORA_PENT19_6,),
    (constants.TEMPORA_PENT20_0,),
    (constants.TEMPORA_PENT20_1,),
    (constants.TEMPORA_PENT20_2,),
    (constants.TEMPORA_PENT20_3,),
    (constants.TEMPORA_PENT20_4,),
    (constants.TEMPORA_PENT20_5,),
    (constants.TEMPORA_PENT20_6,),
    (constants.TEMPORA_PENT21_0,),
    (constants.TEMPORA_PENT21_1,),
    (constants.TEMPORA_PENT21_2,),
    (constants.TEMPORA_PENT21_3,),
    (constants.TEMPORA_PENT21_4,),
    (constants.TEMPORA_PENT21_5,),
    (constants.TEMPORA_PENT21_6,),
    (constants.TEMPORA_PENT22_0,),
    (constants.TEMPORA_PENT22_1,),
    (constants.TEMPORA_PENT22_2,),
    (constants.TEMPORA_PENT22_3,),
    (constants.TEMPORA_PENT22_4,),
    (constants.TEMPORA_PENT22_5,),
    (constants.TEMPORA_PENT22_6,),
    (constants.TEMPORA_PENT23_0,),
    (constants.TEMPORA_PENT23_1,),
    (constants.TEMPORA_PENT23_2,),
    (constants.TEMPORA_PENT23_3,),
    (constants.TEMPORA_PENT23_4,),
    (constants.TEMPORA_PENT23_5,),
    (constants.TEMPORA_PENT23_6,),
)

EMBER_DAYS_SEPTEMBER = (
    (constants.TEMPORA_PENT_3,),
    (),
    (constants.TEMPORA_PENT_5,),
    (constants.TEMPORA_PENT_6,),
)

WEEK_24_AFTER_PENTECOST = (
    (constants.TEMPORA_PENT24_0,),
    (constants.TEMPORA_PENT24_1,),
    (constants.TEMPORA_PENT24_2,),
    (constants.TEMPORA_PENT24_3,),
    (constants.TEMPORA_PENT24_4,),
    (constants.TEMPORA_PENT24_5,),
    (constants.TEMPORA_PENT24_6,),
)

ADVENT = (
    (constants.TEMPORA_ADV1_0,),
    (constants.TEMPORA_ADV1_1,),
    (constants.TEMPORA_ADV1_2,),
    (constants.TEMPORA_ADV1_3,),
    (constants.TEMPORA_ADV1_4,),
    (constants.TEMPORA_ADV1_5,),
    (constants.TEMPORA_ADV1_6,),
    (constants.TEMPORA_ADV2_0,),
    (constants.TEMPORA_ADV2_1,),
    (constants.TEMPORA_ADV2_2,),
    (constants.TEMPORA_ADV2_3,),
    (constants.TEMPORA_ADV2_4,),
    (constants.TEMPORA_ADV2_5,),
    (constants.TEMPORA_ADV2_6,),
    (constants.TEMPORA_ADV3_0,),
    (constants.TEMPORA_ADV3_1,),
    (constants.TEMPORA_ADV3_2,),
    (constants.TEMPORA_ADV3_3,),
    (constants.TEMPORA_ADV3_4,),
    (constants.TEMPORA_ADV3_5,),
    (constants.TEMPORA_ADV3_6,),
    (constants.TEMPORA_ADV4_0,),
    (constants.TEMPORA_ADV4_1,),
    (constants.TEMPORA_ADV4_2,),
    (constants.TEMPORA_ADV4_3,),
    (constants.TEMPORA_ADV4_4,),
    (constants.TEMPORA_ADV4_5,),
)

NATIVITY_OCTAVE_SUNDAY = (
    (constants.TEMPORA_NAT1_0,),
)

NATIVITY_OCTAVE_FERIA = (
    (constants.TEMPORA_NAT1_1,),
)

HOLY_NAME = (
    (constants.TEMPORA_NAT2_0,),
)

CHRIST_KING = (
    (constants.SANCTI_10_DU,),
)

SUNDAY_IN_CHRISTMAS_OCTAVE = (
    (constants.TEMPORA_NAT1_0,),
)

SANCTI = (
    constants.SANCTI_01_01,
    constants.SANCTI_01_05,
    constants.SANCTI_01_06,
    constants.SANCTI_01_11,
    constants.SANCTI_01_13,
    constants.SANCTI_01_14,
    constants.SANCTI_01_14C,
    constants.SANCTI_01_15,
    constants.SANCTI_01_15C,
    constants.SANCTI_01_16,
    constants.SANCTI_01_17,
    constants.SANCTI_01_18,
    constants.SANCTI_01_19,
    constants.SANCTI_01_19C,
    constants.SANCTI_01_20,
    constants.SANCTI_01_21,
    constants.SANCTI_01_22,
    constants.SANCTI_01_23,
    constants.SANCTI_01_23C,
    constants.SANCTI_01_24,
    constants.SANCTI_01_25,
    constants.SANCTI_01_25C,
    constants.SANCTI_01_26,
    constants.SANCTI_01_27,
    constants.SANCTI_01_28,
    constants.SANCTI_01_28C,
    constants.SANCTI_01_29,
    constants.SANCTI_01_30,
    constants.SANCTI_01_31,
    constants.SANCTI_02_01,
    constants.SANCTI_02_02,
    constants.SANCTI_02_03,
    constants.SANCTI_02_04,
    constants.SANCTI_02_05,
    constants.SANCTI_02_06,
    constants.SANCTI_02_06C,
    constants.SANCTI_02_07,
    constants.SANCTI_02_08,
    constants.SANCTI_02_09,
    constants.SANCTI_02_09C,
    constants.SANCTI_02_10,
    constants.SANCTI_02_11,
    constants.SANCTI_02_12,
    constants.SANCTI_02_14,
    constants.SANCTI_02_15,
    constants.SANCTI_02_18,
    constants.SANCTI_02_22,
    constants.SANCTI_02_22C,
    constants.SANCTI_02_23,
    constants.SANCTI_02_24,
    constants.SANCTI_02_27,
    constants.SANCTI_03_04,
    constants.SANCTI_03_06,
    constants.SANCTI_03_07,
    constants.SANCTI_03_08,
    constants.SANCTI_03_09,
    constants.SANCTI_03_10,
    constants.SANCTI_03_12,
    constants.SANCTI_03_17,
    constants.SANCTI_03_18,
    constants.SANCTI_03_19,
    constants.SANCTI_03_21,
    constants.SANCTI_03_24,
    constants.SANCTI_03_25,
    constants.SANCTI_03_27,
    constants.SANCTI_03_28,
    constants.SANCTI_04_11,
    constants.SANCTI_04_13,
    constants.SANCTI_04_14,
    constants.SANCTI_04_17,
    constants.SANCTI_04_21,
    constants.SANCTI_04_22,
    constants.SANCTI_04_23,
    constants.SANCTI_04_24,
    constants.SANCTI_04_25,
    constants.SANCTI_04_25C,
    constants.SANCTI_04_26,
    constants.SANCTI_04_27,
    constants.SANCTI_04_28,
    constants.SANCTI_04_29,
    constants.SANCTI_04_30,
    constants.SANCTI_05_01,
    constants.SANCTI_05_02,
    constants.SANCTI_05_03,
    constants.SANCTI_05_04,
    constants.SANCTI_05_05,
    constants.SANCTI_05_07,
    constants.SANCTI_05_09,
    constants.SANCTI_05_10,
    constants.SANCTI_05_10C,
    constants.SANCTI_05_11,
    constants.SANCTI_05_12,
    constants.SANCTI_05_13,
    constants.SANCTI_05_14,
    constants.SANCTI_05_15,
    constants.SANCTI_05_16,
    constants.SANCTI_05_17,
    constants.SANCTI_05_18,
    constants.SANCTI_05_19,
    constants.SANCTI_05_20,
    constants.SANCTI_05_25,
    constants.SANCTI_05_26,
    constants.SANCTI_05_27,
    constants.SANCTI_05_27C,
    constants.SANCTI_05_27C,
    constants.SANCTI_05_27C,
    constants.SANCTI_05_28,
    constants.SANCTI_05_29,
    constants.SANCTI_05_30,
    constants.SANCTI_05_31,
    constants.SANCTI_05_31C,
    constants.SANCTI_06_01,
    constants.SANCTI_06_02,
    constants.SANCTI_06_04,
    constants.SANCTI_06_05,
    constants.SANCTI_06_06,
    constants.SANCTI_06_09,
    constants.SANCTI_06_10,
    constants.SANCTI_06_11,
    constants.SANCTI_06_12,
    constants.SANCTI_06_12C,
    constants.SANCTI_06_13,
    constants.SANCTI_06_14,
    constants.SANCTI_06_15,
    constants.SANCTI_06_17,
    constants.SANCTI_06_18,
    constants.SANCTI_06_18C,
    constants.SANCTI_06_19,
    constants.SANCTI_06_19C,
    constants.SANCTI_06_20,
    constants.SANCTI_06_21,
    constants.SANCTI_06_22,
    constants.SANCTI_06_23,
    constants.SANCTI_06_24,
    constants.SANCTI_06_25,
    constants.SANCTI_06_26,
    constants.SANCTI_06_28,
    constants.SANCTI_06_29,
    constants.SANCTI_06_30,
    constants.SANCTI_07_01,
    constants.SANCTI_07_02,
    constants.SANCTI_07_02C,
    constants.SANCTI_07_03,
    constants.SANCTI_07_05,
    constants.SANCTI_07_07,
    constants.SANCTI_07_08,
    constants.SANCTI_07_10,
    constants.SANCTI_07_11,
    constants.SANCTI_07_12,
    constants.SANCTI_07_12C,
    constants.SANCTI_07_14,
    constants.SANCTI_07_15,
    constants.SANCTI_07_16,
    constants.SANCTI_07_17,
    constants.SANCTI_07_18,
    constants.SANCTI_07_19,
    constants.SANCTI_07_20,
    constants.SANCTI_07_21,
    constants.SANCTI_07_22,
    constants.SANCTI_07_23,
    constants.SANCTI_07_23C,
    constants.SANCTI_07_24,
    constants.SANCTI_07_25,
    constants.SANCTI_07_25C,
    constants.SANCTI_07_26,
    constants.SANCTI_07_27,
    constants.SANCTI_07_28,
    constants.SANCTI_07_29,
    constants.SANCTI_07_29C,
    constants.SANCTI_07_30,
    constants.SANCTI_07_31,
    constants.SANCTI_08_01,
    constants.SANCTI_08_02,
    constants.SANCTI_08_02C,
    constants.SANCTI_08_04,
    constants.SANCTI_08_05,
    constants.SANCTI_08_06,
    constants.SANCTI_08_06C,
    constants.SANCTI_08_07,
    constants.SANCTI_08_07C,
    constants.SANCTI_08_08,
    constants.SANCTI_08_08C,
    constants.SANCTI_08_09,
    constants.SANCTI_08_09C,
    constants.SANCTI_08_10,
    constants.SANCTI_08_11,
    constants.SANCTI_08_12,
    constants.SANCTI_08_13,
    constants.SANCTI_08_14,
    constants.SANCTI_08_14C,
    constants.SANCTI_08_15,
    constants.SANCTI_08_16,
    constants.SANCTI_08_17,
    constants.SANCTI_08_18,
    constants.SANCTI_08_19,
    constants.SANCTI_08_20,
    constants.SANCTI_08_21,
    constants.SANCTI_08_22,
    constants.SANCTI_08_22C,
    constants.SANCTI_08_23,
    constants.SANCTI_08_24,
    constants.SANCTI_08_25,
    constants.SANCTI_08_26,
    constants.SANCTI_08_27,
    constants.SANCTI_08_28,
    constants.SANCTI_08_28C,
    constants.SANCTI_08_29,
    constants.SANCTI_08_29C,
    constants.SANCTI_08_30,
    constants.SANCTI_08_30C,
    constants.SANCTI_08_31,
    constants.SANCTI_09_01,
    constants.SANCTI_09_02,
    constants.SANCTI_09_03,
    constants.SANCTI_09_05,
    constants.SANCTI_09_08,
    constants.SANCTI_09_09,
    constants.SANCTI_09_10,
    constants.SANCTI_09_11,
    constants.SANCTI_09_12,
    constants.SANCTI_09_14,
    constants.SANCTI_09_15,
    constants.SANCTI_09_16,
    constants.SANCTI_09_16C,
    constants.SANCTI_09_17,
    constants.SANCTI_09_18,
    constants.SANCTI_09_19,
    constants.SANCTI_09_20,
    constants.SANCTI_09_21,
    constants.SANCTI_09_22,
    constants.SANCTI_09_23,
    constants.SANCTI_09_23C,
    constants.SANCTI_09_24,
    constants.SANCTI_09_26,
    constants.SANCTI_09_27,
    constants.SANCTI_09_28,
    constants.SANCTI_09_29,
    constants.SANCTI_09_30,
    constants.SANCTI_10_01,
    constants.SANCTI_10_02,
    constants.SANCTI_10_03,
    constants.SANCTI_10_04,
    constants.SANCTI_10_05,
    constants.SANCTI_10_06,
    constants.SANCTI_10_07,
    constants.SANCTI_10_07C,
    constants.SANCTI_10_08,
    constants.SANCTI_10_08C,
    constants.SANCTI_10_09,
    constants.SANCTI_10_10,
    constants.SANCTI_10_11,
    constants.SANCTI_10_13,
    constants.SANCTI_10_14,
    constants.SANCTI_10_15,
    constants.SANCTI_10_16,
    constants.SANCTI_10_17,
    constants.SANCTI_10_18,
    constants.SANCTI_10_19,
    constants.SANCTI_10_20,
    constants.SANCTI_10_21,
    constants.SANCTI_10_23,
    constants.SANCTI_10_24,
    constants.SANCTI_10_25,
    constants.SANCTI_10_28,
    constants.SANCTI_11_01,
    constants.SANCTI_11_02_1,
    constants.SANCTI_11_02_2,
    constants.SANCTI_11_02_3,
    constants.SANCTI_11_04,
    constants.SANCTI_11_08,
    constants.SANCTI_11_09,
    constants.SANCTI_11_10,
    constants.SANCTI_11_11,
    constants.SANCTI_11_12,
    constants.SANCTI_11_13,
    constants.SANCTI_11_14,
    constants.SANCTI_11_15,
    constants.SANCTI_11_16,
    constants.SANCTI_11_17,
    constants.SANCTI_11_18,
    constants.SANCTI_11_19,
    constants.SANCTI_11_20,
    constants.SANCTI_11_21,
    constants.SANCTI_11_22,
    constants.SANCTI_11_23,
    constants.SANCTI_11_24,
    constants.SANCTI_11_25,
    constants.SANCTI_11_26,
    constants.SANCTI_11_29,
    constants.SANCTI_11_30,
    constants.SANCTI_12_02,
    constants.SANCTI_12_03,
    constants.SANCTI_12_04,
    constants.SANCTI_12_05,
    constants.SANCTI_12_06,
    constants.SANCTI_12_07,
    constants.SANCTI_12_08,
    constants.SANCTI_12_10,
    constants.SANCTI_12_11,
    constants.SANCTI_12_13,
    constants.SANCTI_12_16,
    constants.SANCTI_12_21,
    constants.SANCTI_12_24,
    constants.SANCTI_12_25_1,
    constants.SANCTI_12_25_2,
    constants.SANCTI_12_25_3,
    constants.SANCTI_12_26,
    constants.SANCTI_12_27,
    constants.SANCTI_12_28,
    constants.SANCTI_12_29,
    constants.SANCTI_12_31,
)

TEMPORA_IDS = list(itertools.chain.from_iterable(POST_EPIPHANY +
                                                 FROM_PRE_LENT_TO_POST_PENTECOST +
                                                 EMBER_DAYS_SEPTEMBER +
                                                 WEEK_24_AFTER_PENTECOST +
                                                 ADVENT +
                                                 NATIVITY_OCTAVE_SUNDAY +
                                                 NATIVITY_OCTAVE_FERIA +
                                                 HOLY_NAME +
                                                 CHRIST_KING +
                                                 SUNDAY_IN_CHRISTMAS_OCTAVE))
ALL_IDS = TEMPORA_IDS + list(SANCTI)
