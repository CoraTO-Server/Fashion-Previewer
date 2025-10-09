# Character palette ranges from fashionpreviewer.py
CHARACTER_RANGES = {
    "001": {
        "fashion_1": [range(111, 128)],  # w00-w06: 111-127
        "fashion_2": [range(128, 152)],  # w10-w16: 128-151
        "fashion_3": [range(154, 160)],  # w20-w26: 154-159
        "fashion_4": [range(160, 169)],  # w30-w36: 160-168
        "fashion_5": [range(173, 192)],  # w40-w46: 173-191
        "hair": [range(208, 226)]  # Hair palettes: 208-225
    },
    "002": {
        "fashion_1": [range(111, 128)],  # w00-w06: 111-127
        "fashion_2": [range(128, 137)],  # w10-w16: 128-136
        "fashion_3": [range(140, 144)],  # w20-w26: 140-143
        "fashion_4": [range(144, 154)],  # w30-w36: 144-153
        "fashion_5": [range(160, 172)],  # w40-w46: 160-171
        "fashion_6": [range(176, 185)],  # w50-w56: 176-184
        "hair": [range(208, 226)]  # Hair palettes: 208-225
    },
    "003": {
        "fashion_1": [range(0, 254)],  # w00-w06: 0-253
        "fashion_2": [range(0, 135)],  # w10-w16: 0-134
        "fashion_3": [range(0, 136), range(137, 144)],  # w20-w26: 0-135, 137-143
        "fashion_4": [range(0, 136), range(144, 154)],  # w30-w36: 0-135, 144-153
        "fashion_5": [range(0, 154), range(155, 160)],  # w40-w46: 0-153, 155-159
        "fashion_6": [range(0, 175)],  # w50-w56: 0-174
        "hair": [range(208, 226)]  # Hair palettes: 208-225
    },
    "004": {
        "fashion_1": [range(111, 133)],  # w00-w06: 111-132
        "fashion_2": [range(134, 145)],  # w10-w16: 134-144
        "fashion_3": [range(146, 160)],  # w20-w26: 146-159
        "fashion_4": [range(160, 172)],  # w30-w36: 160-171
        "fashion_5": [range(176, 198)],  # w40-w46: 176-197
        "hair": [range(208, 226)]  # Hair palettes: 208-219
    },
    "005": {
        "fashion_1": [range(111, 119)],  # w00-w06: 111-118
        "fashion_2": [range(122, 128)],  # w10-w16: 122-127
        "fashion_3": [range(128, 139)],  # w20-w26: 128-138
        "fashion_4": [range(140, 144)],  # w30-w36: 140-143
        "fashion_5": [range(144, 208)],  # w40-w46: 144-207
        "hair": [range(208, 226)]  # Hair palettes: 208-225
    },
    "006": {
        "fashion_1": [range(111, 147)],  # w00-w06: 111-146
        "fashion_2": [range(148, 166)],  # w10-w16: 148-165
        "fashion_3": [range(167, 190)],  # w20-w26: 167-189
        "fashion_4": [range(191, 202)],  # w30-w36: 191-201
        "fashion_5": [range(202, 208)],  # w40-w46: 202-207
        "hair": [range(208, 226)]  # Hair palettes: 208-225
    },
    "007": {
        "fashion_1": [range(111, 120)],  # w00-w06: 111-119
        "fashion_2": [range(124, 128)],  # w10-w16: 124-127
        "fashion_3": [range(128, 138)],  # w20-w26: 128-137
        "fashion_4": [range(144, 168)],  # w30-w36: 144-167
        "fashion_5": [range(169, 192)],  # w40-w46: 169-191
        "fashion_6": [range(192, 202)],  # w50-w56: 192-201
        "hair": [range(208, 226)]  # Hair palettes: 208-225
    },
    "008": {
        "fashion_1": [range(0, 95), range(111, 134)],  # w00-w06: 0-94, 111-133
        "fashion_2": [range(137, 144)],  # w10-w16: 137-143
        "fashion_3": [range(144, 151)],  # w20-w26: 144-150
        "hair": [range(208, 226)]  # Hair palettes: 208-225
    },
    "009": {
        "fashion_1": [range(111, 127)],  # w00-w04: 111-126
        "fashion_2": [range(128, 152)],  # w10-w14: 128-151
        "fashion_3": [range(153, 157)],  # w20-w24: 153-156
        "fashion_4": [range(158, 163)],  # w30-w34: 158-162
        "fashion_5": [range(164, 171)],  # w40-w44: 164-170
        "fashion_6": [range(172, 178)],  # w50-w54: 172-177
        "hair": [range(208, 226)]  # Hair palettes: 208-225
    },
    "010": {
        "fashion_1": [range(111, 122)],  # w00-w04: 111-121
        "fashion_2": [range(123, 149)],  # w10-w14: 123-148
        "fashion_3": [range(150, 158)],  # w20-w24: 150-157
        "fashion_4": [range(159, 176)],  # w30-w34: 159-175
        "fashion_5": [range(177, 201)],  # w40-w44: 177-200
        "hair": [range(208, 226)]  # Hair palettes: 208-225
    },
    "011": {
        "fashion_1": [range(0, 110), range(111, 137)],  # w00-w04: 0-109, 111-136
        "fashion_2": [range(0, 137), range(138, 149)],  # w10-w14: 0-136, 138-148
        "fashion_3": [range(0, 149), range(150, 236)],  # w20-w24: 0-148, 150-235
        "fashion_4": [range(0, 177)],  # w30-w34: 0-176
        "fashion_5": [range(0, 177), range(178, 198)],  # w40-w44: 0-176, 178-197
        "hair": [range(208, 226)]  # Hair palettes: 208-225
    },
    "012": {
        "fashion_1": [range(111, 121)],  # w00-w04: 111-120
        "fashion_2": [range(122, 133)],  # w10-w14: 122-132
        "fashion_3": [range(134, 159)],  # w20-w24: 134-158
        "fashion_4": [range(160, 172)],  # w30-w34: 160-171
        "fashion_5": [range(173, 195)],  # w40-w44: 173-194
        "hair": [range(208, 226)]  # Hair palettes: 208-225
    },
    "013": {
        "fashion_1": [range(111, 131)],  # w00-w04: 111-130
        "fashion_2": [range(132, 148)],  # w10-w14: 131-148
        "fashion_3": [range(149, 153)],  # w20-w24: 149-157
        "fashion_4": [range(154, 157)],  # w30-w34: 158-165
        "fashion_5": [range(158, 177)],  # Shoes: 166-176
        "hair": [range(208, 226)]  # Hair palettes: 208-225
    },
    "014": {
        "fashion_1": [range(111, 116)],  # w00-w04: 111-115
        "fashion_2": [range(118, 155)],  # w10-w14: 118-154
        "fashion_3": [range(156, 165)],  # w20-w24: 156-164
        "fashion_4": [range(166, 172)],  # w30-w34: 166-171
        "fashion_5": [range(173, 185)],  # w40-w44: 173-184
        "hair": [range(208, 232)]  # Hair palettes: 208-231
    },
    "015": {
        "fashion_1": [range(111, 123)],  # w00-w04: 111-122
        "fashion_2": [range(124, 132)],  # w10-w14: 124-131
        "fashion_3": [range(133, 143)],  # w20-w24: 133-142
        "fashion_4": [range(144, 149)],  # w30-w34: 144-148
        "fashion_5": [range(150, 164)],  # w40-w44: 150-163
        "hair": [range(208, 226)]  # Hair palettes: 208-225
    },
    "016": {
        "fashion_1": [range(111, 121)],  # w00-w04: 111-120
        "fashion_2": [range(122, 148)],  # w10-w14: 122-147
        "fashion_3": [range(149, 156)],  # w20-w24: 149-155
        "hair": [range(208, 226)]  # Hair palettes: 208-225
    },
    "017": {
        "fashion_1": [range(111, 124)],  # w00-w03: 111-123
        "fashion_2": [range(128, 141)],  # w10-w13: 128-140
        "fashion_3": [range(144, 160)],  # w20-w23: 144-159
        "fashion_4": [range(160, 168), range(170, 176)],  # w30-w33: 160-167, 170-175
        "fashion_5": [range(176, 190)],  # w40-w43, w50: 176-189
        "3rd_job_base": [range(111, 190)],  # 3rd job base fashion: 111-189
        "hair": [range(208, 232)]  # Hair palettes: 208-231
    },
    "018": {
        "fashion_1": [range(111, 113)],  # w00-w03: 111-112
        "fashion_2": [range(116, 149)],  # w10-w13: 116-148
        "fashion_3": [range(150, 157), range(158, 174)],  # w20-w23: 150-156, 158-173
        "fashion_4": [range(176, 181)],  # w30-w33: 176-180
        "fashion_5": [range(181, 184), range(187, 205)],  # w40-w41, w43: 181-183, 187-204
        "fashion_6": [range(187, 205)],  # w50-w51: 187-204
        "3rd_job_base": [range(111, 205)],  # 3rd job base fashion: 111-204
        "hair": [range(208, 231)]  # Hair palettes: 208-230
    },
    "019": {
        "fashion_1": [range(0, 110), range(111, 141)],  # w00-w03: 0-109, 111-140
        "fashion_2": [range(0, 143), range(144, 155)],  # w10-w13: 0-142, 144-154
        "fashion_3": [range(0, 155), range(156, 174)],  # w20-w23: 0-154, 156-173
        "fashion_4": [range(0, 174), range(175, 192)],  # w30-w33: 0-173, 175-191
        "fashion_5": [range(0, 191), range(195, 208)],  # w40-w43: 0-190, 195-207
        "hair": [range(208, 226)]  # Hair palettes: 208-225
    },
    "020": {
        "fashion_1": [range(111, 138)],  # w00-w03: 111-137
        "fashion_2": [range(140, 148)],  # w10-w13: 140-147
        "fashion_3": [range(150, 158)],  # w20-w23: 150-157
        "fashion_4": [range(160, 172)],  # w30-w33: 160-171
        "fashion_5": [range(173, 192)],  # w40-w43: 173-191
        "3rd_job_base": [range(111, 192)],  # 3rd job base fashion: 111-191
        "hair": [range(208, 219)]  # Hair palettes: 208-218
    },
    "021": {
        "fashion_1": [range(111, 132)],  # w00-w03: 111-131
        "fashion_2": [range(133, 137)],  # w10-w13: 133-136
        "fashion_3": [range(140, 152)],  # w20-w23: 140-151
        "fashion_4": [range(153, 168)],  # w30-w33: 153-167
        "fashion_5": [range(173, 185)],  # w40: 173-184
        "hair": [range(208, 226)]  # Hair palettes: 208-225
    },
    "022": {
        "fashion_1": [range(111, 137)],  # w00-w03: 111-136
        "fashion_2": [range(140, 161)],  # w10-w13: 140-160
        "fashion_3": [range(164, 177)],  # w20-w23: 164-176
        "fashion_4": [range(180, 198)],  # w30-w33: 180-197
        "fashion_5": [range(158, 177)],  # w40: 158-176
        "3rd_job_base": [range(111, 198)],  # 3rd job base fashion: 111-197
        "hair": [range(208, 232)]  # Hair palettes: 208-231
    },
    "023": {
        "fashion_1": [range(111, 125), range(126, 144)],  # w00-w03: 111-124, 126-143
        "fashion_2": [range(144, 148)],  # w10-w13: 144-147
        "fashion_3": [range(150, 156), range(160, 186)],  # w20-w23: 150-155, 160-185
        "fashion_4": [range(188, 194)],  # w30-w33, w40-w41: 188-193
        "hair": [range(208, 226)]  # Hair palettes: 208-225
    },
    "024": {
        "fashion_1": [range(111, 131)],  # 111-130
        "fashion_2": [range(134, 149)],  # 134-148
        "fashion_3": [range(150, 165)],  # 150-164
        "fashion_4": [range(166, 174)],  # 166-173
        "fashion_5": [range(1, 34), range(111, 131), range(134, 149), range(150, 165), range(166, 174), range(176, 182), range(208, 219)],  # w02, w12, w22, w32, w42 pattern
        "fashion_6": [range(176, 182)],  # w40, w41, w43 pattern
        "hair": [range(208, 226)]  # Hair palettes: 208-225
    },
    # Paula characters (both number formats)
    "025": {  # Same as 100
        "fashion_1": [range(111, 142)],  # group 1: 111-141
        "fashion_2": [range(142, 154)],  # group 2: 142-153
        "fashion_3": [range(154, 168)],  # group 3: 154-167
        "fashion_4": [range(168, 174), range(189, 193)],  # group 4: 168-173 AND 189-192
        "fashion_5": [range(174, 177)],  # group 5: 174-176
        "fashion_6": [range(177, 189)],  # group 6: 177-188
        "fashion_7": [range(189, 193)],  # group 7: 189-192
        "hair": [range(208, 226)]  # Hair palettes: 208-225
    },
    "026": {  # Same as 101
        "fashion_1": [range(111, 142)],  # w00-w04: 111-141
        "fashion_2": [range(142, 156)],  # w10-w14: 142-155
        "fashion_3": [range(156, 174)],  # w20-w24: 156-173
        "fashion_4": [range(174, 178)],  # w30-w34: 174-177
        "fashion_5": [range(178, 190)],  # w40-w44: 178-189
        "fashion_6": [range(190, 193)],  # w50-w54: 190-192
        "hair": [range(208, 226)]  # Hair palettes: 208-225
    },
    "027": {  # Same as 102
        "fashion_1": [range(111, 118)],  # w00-w03: 111-117
        "fashion_2": [range(119, 147)],  # w10-w13: 119-146
        "fashion_3": [range(148, 151)],  # w20-w23: 148-150
        "fashion_4": [range(152, 166)],  # w30-w33: 152-165
        "fashion_5": [range(167, 175)],  # w40-w43: 167-174
        "fashion_6": [range(176, 182)],  # w50-w53: 176-181
        "fashion_7": [range(183, 192)],  # w60-w63: 183-191
        "fashion_8": [range(192, 208)],  # w70-w73: 192-207
        "hair": [range(208, 226)]  # Hair palettes: 208-225
    },
    "100": {  # Same as 025
        "fashion_1": [range(111, 142)],  # group 1: 111-141
        "fashion_2": [range(142, 154)],  # group 2: 142-153
        "fashion_3": [range(154, 168)],  # group 3: 154-167
        "fashion_4": [range(168, 174), range(189, 193)],  # group 4: 168-173 AND 189-192
        "fashion_5": [range(174, 177)],  # group 5: 174-176
        "fashion_6": [range(177, 189)],  # group 6: 177-188
        "fashion_7": [range(189, 193)],  # group 7: 189-192
        "hair": [range(208, 226)]  # Hair palettes: 208-225
    },
    "101": {  # Same as 026
        "fashion_1": [range(111, 142)],  # w00-w04: 111-141
        "fashion_2": [range(142, 156)],  # w10-w14: 142-155
        "fashion_3": [range(156, 174)],  # w20-w24: 156-173
        "fashion_4": [range(174, 178)],  # w30-w34: 174-177
        "fashion_5": [range(178, 190)],  # w40-w44: 178-189
        "fashion_6": [range(190, 193)],  # w50-w54: 190-192
        "hair": [range(208, 226)]  # Hair palettes: 208-225
    },
    "102": {  # Same as 027
        "fashion_1": [range(111, 118)],  # w00-w03: 111-117
        "fashion_2": [range(119, 147)],  # w10-w13: 119-146
        "fashion_3": [range(148, 151)],  # w20-w23: 148-150
        "fashion_4": [range(152, 166)],  # w30-w33: 152-165
        "fashion_5": [range(167, 175)],  # w40-w43: 167-174
        "fashion_6": [range(176, 182)],  # w50-w53: 176-181
        "fashion_7": [range(183, 192)],  # w60-w63: 183-191
        "fashion_8": [range(192, 208)],  # w70-w73: 192-207
        "hair": [range(208, 226)]  # Hair palettes: 208-225
    }
}
