stage_dict = {}

asteroid_field = [('meteor', 'w/e', False, 20), ('meteor', 'w/e', False, 10), ('meteor', 'w/e', False, 10), ('meteor', 'w/e', False, 10),
                  ('meteor', 'w/e', False, 10), ('meteor', 'w/e', False, 10), ('meteor', 'w/e', False, 10)]
stage_dict['asteroid_field'] = asteroid_field

#stage1 = []
s1_wave1 = [('enemyShip1', 'down_DNA', False), ('enemyShip1', 'up_DNA', False)]
s1_wave2 = [('enemyShip1', 'down_Zig', False), ('enemyShip1', 'up_Zig', False)]
stage1 = [s1_wave1, s1_wave2]

stage_dict["stage1"] = stage1