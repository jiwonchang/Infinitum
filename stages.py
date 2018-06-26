stage_dict = {}

asteroid_field = [('meteor', 'w/e', False, 20), ('meteor', 'w/e', False, 10), ('meteor', 'w/e', False, 10), ('meteor', 'w/e', False, 10),
                  ('meteor', 'w/e', False, 10), ('meteor', 'w/e', False, 10), ('meteor', 'w/e', False, 10)]
stage_dict['asteroid_field'] = asteroid_field

#stage1 = []
s1_wave00 = [('enemySmuggler1', 'topLeftDown_Rand', False, 3)]
s1_wave01 = [('enemySmuggler1', 'topRightDown_Rand', False, 3)]
s1_wave02 = [('enemySmuggler1', 'topLeftDown_Rand', False, 4)]
s1_wave03 = [('enemySmuggler1', 'topLeftDown_Rand', False, 2), ('enemySmuggler1', 'topRightDown_Rand', False, 2)]
s1_wave04 = [('enemySmuggler1', 'topLeftDown_Rand', False, 3), ('enemySmuggler1', 'topRightDown_Rand', False, 3)]
s1_wave05 = [('enemySmuggler1', 'topLeftDown_Rand', False, 3), ('enemySmuggler1', 'topRightDown_Rand', False, 3)]
s1_wave06 = [('enemySmuggler1', 'topLeftDown_Rand', False, 5), ('enemySmuggler1', 'topRightDown_Rand', False, 5)]
s1_wave07 = [('enemySmuggler2', 'topLeft_Down', False, 1), ('enemySmuggler2', 'topRight_Down', False, 1)]
s1_wave08 = [('enemySmuggler1', 'topLeftDown_Rand', False, 2), ('enemySmuggler1', 'topRightDown_Rand', False, 2)]
s1_wave10 = ['dialogue', ('enemySmugglerLieut', 'topDown_SLieut', False, 1)]
#('smugglerLieut', 'w/e', False, 1)
stage1 = [s1_wave00, s1_wave01, s1_wave02, s1_wave03, s1_wave04, s1_wave05, s1_wave06, s1_wave07, 'empty wave', s1_wave08, s1_wave04, s1_wave10]

s2_wave7 = [('enemyCruiser1', 'topLeft_Cruiser', False, 1), ('enemyCruiser1', 'topRight_Cruiser', False, 1)]
s2_wave0 = [('enemyFighter1', 'topLeftDown_Rand', False, 5), ('enemyFighter1', 'topRightDown_Rand', False, 5)]
s2_wave1 = [('enemyFighter1', 'topDown_0', False, 5), ('enemyFighter1', 'topDown_0_pair', False, 5)]
s2_wave2 = [('enemyFighter1', 'topLeft_Dip', False, 10)]
s2_wave3 = [('enemyShip1', 'topLeft_DNA', False, 10)]
s2_wave4 = [('enemyShip1', 'topRight_DNA', False, 10)]
s2_wave5 = [('enemyShip1', 'topLeft_Z', False, 10)]
s2_wave6 = [('enemyShip1', 'topRight_Z', False, 10)]
s2_wave8 = [('enemyBomber', 'topLeft_Bomber', False, 5)]
s2_wave9 = [('kamikaze', 'topLeft_Kami', False, 5)]
stage2 = [s2_wave9, s2_wave8, s2_wave7, s2_wave3, s2_wave1, s2_wave2, s2_wave0, s2_wave4, s2_wave5, s2_wave6]

stage_dict["stage1"] = stage1
stage_dict["stage2"] = stage2

#dialog_name_box_dict = {}
dialog_box_dict = {}

#d_name_stage1 = [['???'], ['Smuggler', 'Lieutenant'], ['Aethan'], ['Smuggler', 'Lieutenant']]
d_stage1 = [["???:", "That's about far enough.", "I am one of Victor's Lieutenants, punk."], ["Smuggler Lieutenant:", "Who the hell do you think you are?", "I suggest you get lost. Now."],
            ["Aethan:", "I'm Lieutenant Aethan of the Intergalactic", "Republic Army."], ["Aethan:", "Surrender now and give up Victor's", "location, and I will spare your life."],
            ["Smuggler Lieutenant:", "Ha! There's no chance in hell I'll betray", "the boss."], ["Smuggler Lieutenant:", "At any rate, you're going to pay for", "killing my men!"]]
#dialog_name_box_dict["stage1"] = d_name_stage1
dialog_box_dict["stage1"] = d_stage1