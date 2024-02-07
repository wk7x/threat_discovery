import random
import streamlit as st
# talent toggles
# holy
Improved_SoR = False
Improved_BoW = False
Divine_Strength = True
Divine_Intellect = True
Holy_Power = False
# prot
Precision = True
Improved_RF = True
# ret
Conviction_Points = 0  # 0 to 5
Improved_Judge = True
Improved_Crusader = False
Deflection = False
Benediction = True
Improved_Ret_Aura = False
Two_Hand_Spec = False
Vengeance = False

# abilities toggle
Consecration = True
Seal = "sor"  # sor, soc or som
Divine_Storm = False
Exorcism = True
Holy_Shock = False
Divine_Favor = False
Ret_Aura = True

Sheath = True
Infusion = False

Guarded_By_Light = False
Art_Of_War = True

# weapon values
Weapon_Min = 17
Weapon_Max = 32
Weapon_Speed = 1.3
Weapon_Enchant_Bonus = 10

Weapon_Strength = 3
Weapon_Intellect = 0
Weapon_Agility = 0
Weapon_SP = 0
Handedness = 1  # 1 or 2
Racial_Bonus = True

# stat values
Gear_Strength = 221  # before talent, buff, weapon stats
Gear_Agi = 111  # before buff, weapon stats
Gear_AP = 48
Bonus_SP = 0
Bonus_Crit = 2 / 100  # as decimal
Bonus_Skill = 0
Spell_Crit = 6 / 100  # as decimal
Base_Parry = 5 / 100  # as decimal

Bonus_Hit = 2 /100  # as decimal
Gear_Intellect = 0

Use_Total_Stats = True  # toggle this to use insert total stats (both gear and base at once)
Total_Int = 51
Total_Str = 221
Total_Agi = 111

# raid buffs
Kings = True

BoM = False
Horn = True

Sanctity_Aura = False
WB = True
Battle_Shout = True
WF = True
Judge_Of_Crusader = True
Arcane_Intellect = True
BoW = True
Judge_Of_Wisdom = True
MoW = True
LotP = True

# boss values
Boss_Dodge = 6 / 100  # as decimal
Boss_Parry = 4 / 100  # as decimal
Boss_Armor_Mitigation = 6 / 100  # as decimal
Enemy_Speed = 2

# calc setting
AoW_Judge_Proc = True
Extended_Details = True

# statics at 40
Base_Mana = 987
Base_Strength = 70
Base_Intellect = 49
Boss_Level = 42
Player_Level = 40
Melee_Crit_Per_Agi = 0.0675 / 100
Base_Melee_Crit = 0.665 / 100
Base_Agi = 46


# utility functions
def mult_toggler(boolean, value):
    if boolean:
        return value
    else:
        return 1


def add_toggler(boolean, value):
    if boolean:
        return value
    else:
        return 0


def chance(p):
    random_number = random.random()
    if p > random_number:
        return True
    else:
        return False


def seal_enabler(this_seal, requested_seal):
    if requested_seal != this_seal:
        return 0
    else:
        return 1


def down_ranked(lower_rank_dps, higher_rank_dps):
    if lower_rank_dps >= higher_rank_dps:
        return True
    else:
        return False


def toggle_checker(bom, horn, aow, guarded, infusion, sheath, seal, extra_hit, extra_crit):
    if bom and horn:
        print("Cant have both BOM and Horn buff.")
        exit()
    if aow and guarded:
        print("Can't have AoW and Guarded runes at once.")
        exit()
    if infusion and sheath:
        print("Can't have Infusion and Sheath at once")
        exit()
    if seal not in ["sor", "soc", "som"]:
        print("Invalid seal name.")
        exit()
    if extra_hit > 1:
        print("Invalid hit value, use decimals.")
        exit()
    if extra_crit > 1:
        print("Invalid crit value, use decimals.")
        exit()


# art of war sim
def aow_infusion_expected_cd(speed, melee_crit, imp_judge, aow_judge_proc, seal, exo_used, hs_used, aow, infusion):
    crit_chance = melee_crit

    gcd = 1.5
    on_gcd = False
    gcd_timer = 0

    exo_cd = 15
    exo_on_cd = False
    exo_cd_timer = 0

    hs_cd = 30
    hs_on_cd = False
    hs_cd_timer = 0

    swing_cd = speed
    swing_on_cd = False
    swing_timer = 0

    judge_cd = 10 - add_toggler(imp_judge, 2)
    judge_on_cd = False
    judge_timer = 0

    exorcism_counter = 0
    holy_shock_counter = 0

    t = 0
    target_time = 10 ** 3
    while True:
        if not exo_on_cd and not on_gcd and exo_used:
            exo_on_cd = True
            exo_cd_timer = exo_cd

            on_gcd = True
            gcd_timer = gcd

            exorcism_counter += 1

        if not hs_on_cd and not on_gcd and hs_used:
            hs_on_cd = True
            hs_cd_timer = hs_cd

            on_gcd = True
            gcd_timer = gcd

            holy_shock_counter += 1

            if chance(crit_chance) and infusion:
                if exo_on_cd and exo_used:
                    exo_on_cd = False
                    exo_cd_timer = 0
                hs_on_cd = False
                hs_cd_timer = 0

        if not swing_on_cd:
            swing_on_cd = True
            swing_timer = swing_cd
            if chance(crit_chance) and aow:
                if exo_on_cd and exo_used:
                    exo_on_cd = False
                    exo_cd_timer = 0
                if hs_on_cd and hs_used:
                    hs_on_cd = False
                    hs_cd_timer = 0

        if not judge_on_cd and not on_gcd:
            judge_on_cd = True
            judge_timer = judge_cd

            on_gcd = True
            gcd_timer = gcd

            if chance(crit_chance) and aow_judge_proc and seal != "sor" and aow:
                if exo_on_cd and exo_used:
                    exo_on_cd = False
                    exo_cd_timer = 0
                if hs_on_cd and hs_used:
                    hs_on_cd = False
                    hs_cd_timer = 0

        if exo_on_cd:
            exo_cd_timer = round(exo_cd_timer - 0.1, ndigits=1)
            if exo_cd_timer == 0:
                exo_on_cd = False

        if hs_on_cd:
            hs_cd_timer = round(hs_cd_timer - 0.1, ndigits=1)
            if hs_cd_timer == 0:
                hs_on_cd = False

        if on_gcd:
            gcd_timer = round(gcd_timer - 0.1, ndigits=1)
            if gcd_timer == 0:
                on_gcd = False

        if swing_on_cd:
            swing_timer = round(swing_timer - 0.1, ndigits=1)
            if swing_timer == 0:
                swing_on_cd = False

        if judge_on_cd:
            judge_timer = round(judge_timer - 0.1, ndigits=1)
            if judge_timer == 0:
                judge_on_cd = False

        t = round(t + 0.1, ndigits=1)

        if t == target_time:
            break

    if exo_used:
        new_exo_cd = t / exorcism_counter
    else:
        new_exo_cd = exo_cd
    if hs_used:
        new_hs_cd = t / holy_shock_counter
    else:
        new_hs_cd = hs_cd
    return [new_exo_cd, new_hs_cd]


# mechanics functions
def glance_prob(boss_level, player_level, skill_bonus):
    boss_defense = 5 * boss_level
    base_weapon_skill = 5 * player_level
    weapon_skill = base_weapon_skill + skill_bonus
    output = 0.1 + (boss_defense - min(weapon_skill, base_weapon_skill)) * 0.02
    return output


def glance_reduction_func(boss_level, player_level, skill_bonus):
    weapon_skill = 5 * player_level + skill_bonus
    boss_defense = 5 * boss_level
    delta = boss_defense - weapon_skill
    if delta <= 5:
        return 0.05
    elif round(delta, ndigits=1) == 10:
        return 0.15
    else:
        print("Unexpected glance reduction.")
        exit()


def melee_miss_prob(boss_level, player_level, skill_bonus, precision, extra_hit):
    weapon_skill = 5 * player_level + skill_bonus
    boss_defense = 5 * boss_level
    delta = boss_defense - weapon_skill

    if delta < 0:
        print("Wrong level values.")
        exit()
    if delta >= 11:
        return (5 + 0.2 * delta) / 100 - add_toggler(precision, 3 / 100) - extra_hit
    elif 10 >= delta:
        return (5 + 0.1 * delta) / 100 - add_toggler(precision, 3 / 100) - extra_hit


def spell_miss_prob(boss_level, player_level, extra_hit):
    level_delta = boss_level - player_level
    if level_delta == 1:
        base_miss = 5 / 100
    elif level_delta == 2:
        base_miss = 6 / 100
    elif level_delta == 3:
        base_miss = 17 / 100
    else:
        print("Unexpected level delta.")
        exit()
    output = base_miss - extra_hit
    return output


def max_mana(intellect):
    base_mana = Base_Mana
    mana = base_mana + 20 + (intellect - 20) * 15
    return mana


def attack_power(strength, gear_ap, bom, battle_shout):
    level = 40
    class_ap = 3 * level - 20

    output = 2 * strength + class_ap + gear_ap + add_toggler(bom, 85) + add_toggler(battle_shout, 85)

    return output


def spell_power(ap, bonus_sp, sheath, weapon_sp, wb):
    output = bonus_sp + add_toggler(sheath, 0.3 * ap) + weapon_sp + add_toggler(wb, 42)
    print("Spellpower:", output)
    return output


def base_melee_hit(ap, weapon_max, weapon_min, weapon_speed, wep_enchant_bonus):
    base = (weapon_max + weapon_min) / 2
    scale = ap * weapon_speed / 14
    return base + scale + wep_enchant_bonus


def special_melee_hit(ap, weapon_max, weapon_min, wep_enchant_bonus, handedness):
    base = (weapon_max + weapon_min) / 2
    if handedness == 2:
        coefficient = 3.3
    elif handedness == 1:
        coefficient = 2.4
    else:
        print("Unexpected handedness.")
        exit()
    scale = ap * coefficient / 14
    return base + scale + wep_enchant_bonus


def armor_coefficient(armor_mitigation):
    return 1 - armor_mitigation


def evasion_coefficient(enemy_dodge_chance, enemy_parry_chance, miss_chance):
    dodge_coefficient = 1 - enemy_dodge_chance
    parry_coefficient = 1 - enemy_parry_chance
    miss_coefficient = 1 - miss_chance
    return dodge_coefficient * parry_coefficient * miss_coefficient


def melee_crit_chance(extra_crit, agi, conviction_points, leader):
    base_crit = Base_Melee_Crit
    crit_per_agi = Melee_Crit_Per_Agi
    crit_from_agi = crit_per_agi * agi
    extra_crit = extra_crit + conviction_points/100 + add_toggler(leader, 3/100)
    output = crit_from_agi + base_crit + extra_crit
    return output


def crit_coefficient(crit_chance):
    return 1 + crit_chance


def holy_threat_coefficient(imp_rf):
    if imp_rf:
        return 2.886
    else:
        return 2.22


# seals
def sor_seal_three(speed, sp, imp_sor, handedness):
    if handedness == 1:
        base = 5 * speed - 1
    else:
        base = 6.25 * speed - 1.12
    scale = 0.18 * sp
    return base * mult_toggler(imp_sor, 1.15) + scale


def sor_seal_five(speed, sp, imp_sor, handedness):
    if handedness == 1:
        base = 10 * speed - 1.5
    else:
        base = 11.25 * speed + 1.3
    if handedness == 1:
        scale = 0.1 * sp
    else:
        scale = 1.2 * sp
    return base * mult_toggler(imp_sor, 1.15) + scale


def sor_judge_three(sp, imp_sor):
    base = (53 + 58) / 2
    scale = 0.5 * sp
    return base * mult_toggler(imp_sor, 1.15) + scale


def sor_judge_five(sp, imp_sor):
    base = (96 + 105) / 2
    scale = 0.5 * sp
    return base * mult_toggler(imp_sor, 1.15) + scale


def soc_seal(melee, neutral_sp, holy_sp):
    base = 0.7 * melee
    scale = 0.2 * neutral_sp + 0.29 * holy_sp
    return base + scale


def soc_judge_three(sp, in_cap):
    if in_cap:
        base = (248 + 269) / 2
    else:
        base = (124 + 135) / 2
    scale = 0.43 * sp
    return base + scale


def som_seal(melee):
    return 0.3 * melee


def som_judge(melee):
    return 0.7 * melee


# other abilities
def holy_shock(sp):
    base = (204 + 220) / 2
    scale = 0.43 * sp
    return base + scale


def consecration(sp):
    base = 192
    scale = 0.336 * sp
    return base + scale


def exorcism_dmg(sp):
    base = (227 + 255) / 2
    scale = 0.43 * sp
    return base + scale


def divine_storm(melee):
    return 1.1 * melee


def divine_storm_heal(melee):
    return 0.25 * melee * 1.1


# threat calculator
def threat_calculator(weapon_speed, gear_agi, aow_judge_proc, wb, imp_sor, imp_rf, imp_judge, art_of_war,
                      conviction_points, cons, seal, gear_strength, gear_ap, kings, bom, battle_shout, divine_strength,
                      bonus_sp, sheath, weapon_enchant_bonus, weapon_min, weapon_max, extra_crit, precision, boss_dodge,
                      boss_parry, armor_mitigation, ds, name, spell_crit, ret_aura, boss_speed, wf,
                      deflection, base_parry, exorcism, shock, crusader_judge, weapon_sp, weapon_str, benediction,
                      guarded, arcane, gear_int, bow, wis_judge, holy_power, imp_bow, divine_favor,
                      divine_int, handedness, imp_crusader, imp_ret, two_hand_spec, sanctity_aura, vengeance, racial,
                      extra_wep_skill, extra_hit, horn, mark, infusion, leader, wep_agi, wep_int):

    # debugger
    toggle_checker(bom=bom, horn=horn, aow=art_of_war, guarded=guarded, infusion=infusion, sheath=sheath, seal=seal,
                   extra_crit=extra_crit, extra_hit=extra_hit)

    # stats
    skill_bonus = add_toggler(racial, 5) + extra_wep_skill

    if Use_Total_Stats:
        total_strength = Total_Str
    else:
        total_strength = Base_Strength + gear_strength + weapon_str

    strength = ((total_strength + add_toggler(horn, 40) + add_toggler(mark, 8)) *
                mult_toggler(kings, 1.1) * mult_toggler(divine_strength, 1.1))

    if Use_Total_Stats:
        total_agility = Total_Agi
    else:
        total_agility = gear_agi + Base_Agi + wep_agi

    agility = (total_agility + add_toggler(horn, 40) + add_toggler(mark, 8)) * mult_toggler(kings, 1.1)

    melee_crit = melee_crit_chance(extra_crit=extra_crit, agi=agility, conviction_points=conviction_points,
                                   leader=leader)

    melee_crit_c = crit_coefficient(crit_chance=melee_crit)
    spell_crit = spell_crit + add_toggler(holy_power, 5 / 100) + add_toggler(wb, 3 / 100)
    spell_crit_c = 1 + 0.5 * spell_crit

    ap = attack_power(strength=strength, gear_ap=gear_ap, bom=bom, battle_shout=battle_shout)

    holy_sp = add_toggler(crusader_judge, 80 * mult_toggler(imp_crusader, 1.15))
    neutral_sp = spell_power(ap=ap, bonus_sp=bonus_sp, sheath=sheath, weapon_sp=weapon_sp, wb=wb)
    sp = neutral_sp + holy_sp

    if Use_Total_Stats:
        total_intellect = Total_Int
    else:
        total_intellect = Base_Intellect + gear_int + wep_int

    intellect = ((total_intellect + add_toggler(arcane, 15) + add_toggler(mark, 8))
                 * mult_toggler(kings, 1.1) * mult_toggler(divine_int, 1.1))

    mana = max_mana(intellect=intellect)
    base_mana = Base_Mana

    # cds
    melee_cd = weapon_speed * mult_toggler(wb, 0.9)

    cons_cd = 8

    exo_hs_cd_sim = aow_infusion_expected_cd(speed=melee_cd, melee_crit=melee_crit,
                                             imp_judge=imp_judge,
                                             aow_judge_proc=aow_judge_proc, seal=seal,
                                             exo_used=exorcism, hs_used=shock, aow=art_of_war, infusion=infusion)

    holy_shock_cd = (30 * mult_toggler(art_of_war, 0)
                     + exo_hs_cd_sim[1] * mult_toggler(not art_of_war, 0))

    exorcism_cd = (15 * mult_toggler(art_of_war, 0)
                   + exo_hs_cd_sim[0] * mult_toggler(not art_of_war, 0))

    divine_favor_cd = 30 * 4

    divine_storm_cd = 10

    judge_cd = 10 - add_toggler(imp_judge, 2)

    # boss mitigation
    melee_miss_chance = melee_miss_prob(boss_level=Boss_Level, player_level=Player_Level, skill_bonus=skill_bonus,
                                        precision=precision, extra_hit=extra_hit)
    spell_miss_chance = spell_miss_prob(boss_level=Boss_Level, player_level=Player_Level, extra_hit=extra_hit)

    evasion_c = evasion_coefficient(enemy_dodge_chance=boss_dodge, enemy_parry_chance=boss_parry,
                                    miss_chance=melee_miss_chance)

    armor_c = armor_coefficient(armor_mitigation=armor_mitigation)

    spell_miss_c = 1 - spell_miss_chance

    glance_chance = 0.3
    glance_reduction = glance_reduction_func(boss_level=Boss_Level, player_level=Player_Level, skill_bonus=skill_bonus)
    reduction_coefficient = 1 - glance_reduction
    glance_c = glance_chance * reduction_coefficient + (1 - glance_chance)

    # procs per per sec
    wf_proc_chance = 0.2
    wf_pps = wf_proc_chance * 1 / melee_cd

    extra_hit_per_parry = 0.24
    parry_per_sec = (base_parry + add_toggler(deflection, 5 / 100)) / boss_speed
    parry_hit_per_sec = extra_hit_per_parry * parry_per_sec

    soc_p = 7 / 60 * weapon_speed
    soc_pps = 7 / 60 + (1 - soc_p) * wf_proc_chance * soc_p / melee_cd * mult_toggler(not wf, 0)

    vengeance_pps = ((1 / melee_cd + add_toggler(wf, 1 / wf_pps) + 1 / parry_hit_per_sec +
                      add_toggler(seal == "soc", 1 / soc_pps) + add_toggler(seal == "som", 1 / melee_cd) +
                      add_toggler(ds, 1 / divine_storm_cd)) * melee_crit_c +
                     (1 / judge_cd + add_toggler(exorcism, 1 / exorcism_cd)) * spell_crit_c)

    # damage
    sanctity_c = mult_toggler(sanctity_aura, 1.1)
    two_hand_spec_c = mult_toggler(handedness == 2 and two_hand_spec, 1.06)
    infusion_c = mult_toggler(infusion, 1.2)
    if vengeance_pps >= 1 / 8:
        vengeance_c = mult_toggler(vengeance, 1.15)
    else:
        vengeance_c = mult_toggler(vengeance, 1.2 * vengeance_pps + 1)

    base_melee = base_melee_hit(ap=ap, weapon_min=weapon_min, weapon_max=weapon_max, weapon_speed=weapon_speed,
                                wep_enchant_bonus=weapon_enchant_bonus)

    special_melee = special_melee_hit(ap=ap, weapon_max=weapon_max, weapon_min=weapon_min,
                                      wep_enchant_bonus=weapon_enchant_bonus, handedness=handedness)

    melee = base_melee * evasion_c * armor_c * glance_c * melee_crit_c * two_hand_spec_c * vengeance_c

    wf_hit = melee + 0.2 * ap * weapon_speed / 14 * evasion_c * melee_crit_c * glance_c * two_hand_spec_c * vengeance_c
    wf_dps = wf_pps * wf_hit * mult_toggler(not wf, 0)

    melee_dps = melee / melee_cd + melee * parry_hit_per_sec + wf_dps

    cons_dps = mult_toggler(not cons, 0) * consecration(sp) / cons_cd * spell_miss_c * sanctity_c * vengeance_c

    exorcism_dps = (mult_toggler(not exorcism, 0) * exorcism_dmg(sp) / exorcism_cd * spell_crit_c * spell_miss_c
                    * sanctity_c * vengeance_c)

    holy_shock_damage = holy_shock(sp) * spell_miss_c * spell_crit_c
    holy_shock_dps_without_df = holy_shock_damage / holy_shock_cd
    cd_ratio = divine_favor_cd / holy_shock_cd
    holy_shock_dps_with_df = ((cd_ratio - 1) * holy_shock_damage + 1.5 * holy_shock(
        sp) * spell_miss_c) / divine_favor_cd
    if divine_favor:
        holy_shock_dps = (holy_shock_dps_with_df * mult_toggler(not shock, 0) * sanctity_c * vengeance_c
                          * infusion_c)
    else:
        holy_shock_dps = (holy_shock_dps_without_df * mult_toggler(not shock, 0) * sanctity_c * vengeance_c
                          * infusion_c)

    sor_seal_three_dmg = sor_seal_three(speed=weapon_speed, sp=sp, imp_sor=imp_sor, handedness=handedness) * evasion_c
    sor_judge_three_dmg = sor_judge_three(sp=sp, imp_sor=imp_sor) * spell_crit_c * spell_miss_c

    sor_seal_five_dmg = sor_seal_five(speed=weapon_speed, sp=sp, imp_sor=imp_sor, handedness=handedness) * evasion_c
    sor_judge_five_dmg = sor_judge_five(sp=sp, imp_sor=imp_sor) * spell_crit_c * spell_miss_c

    sor_three_dps = sor_judge_three_dmg / judge_cd + sor_seal_three_dmg * (1 / melee_cd + parry_hit_per_sec + wf_pps)
    sor_five_dps = sor_judge_five_dmg / judge_cd + sor_seal_five_dmg * (1 / melee_cd + parry_hit_per_sec + wf_pps)

    sor_dps = max(sor_three_dps, sor_five_dps) * seal_enabler("sor", seal) * sanctity_c * vengeance_c

    soc_seal_dmg = (soc_seal(melee=base_melee, neutral_sp=neutral_sp, holy_sp=holy_sp) * evasion_c * melee_crit_c *
                    two_hand_spec_c)
    soc_judge_dmg = soc_judge_three(sp=sp, in_cap=False) * melee_crit_c * spell_miss_c

    soc_dps = ((soc_seal_dmg * soc_pps + soc_judge_dmg / judge_cd) * seal_enabler("soc", seal) *
               sanctity_c * vengeance_c)

    som_seal_dmg = som_seal(melee=base_melee) * evasion_c * melee_crit_c * two_hand_spec_c
    som_judge_dmg = som_judge(melee=base_melee) * melee_crit_c * spell_miss_c

    som_dps = (som_seal_dmg * (parry_hit_per_sec + 1 / melee_cd + wf_pps)
               + som_judge_dmg / judge_cd) * seal_enabler("som", seal) * sanctity_c * vengeance_c

    divine_storm_dmg = divine_storm(melee=special_melee) * evasion_c * armor_c * melee_crit_c
    divine_storm_dps = divine_storm_dmg / divine_storm_cd * mult_toggler(not ds, 0) * two_hand_spec_c * vengeance_c

    ret_aura_damage = 12 * mult_toggler(imp_ret, 1.5)
    ret_aura_dps = ret_aura_damage / boss_speed * mult_toggler(not ret_aura, 0) * sanctity_c * vengeance_c

    holy_dps = exorcism_dps + cons_dps + som_dps + soc_dps + sor_dps + ret_aura_dps + holy_shock_dps
    non_holy_dps = divine_storm_dps + melee_dps

    # heal
    ds_heal = divine_storm_heal(melee=special_melee)
    ds_hps = ds_heal / divine_storm_cd

    # mana expenditure
    judge_mana = 20
    judge_mps = judge_mana / judge_cd

    sor_three_mana = 60
    sor_five_mana = 120

    if down_ranked(sor_three_dps, sor_five_dps):
        sor_mana = sor_three_mana
    else:
        sor_mana = sor_five_mana
    sor_mps = sor_mana / judge_cd * seal_enabler("sor", seal)

    soc_mana = 140
    soc_mps = soc_mana / judge_cd * seal_enabler("soc", seal)

    som_mana = 0.04 * base_mana
    som_mps = som_mana / judge_cd * seal_enabler("som", seal)

    seal_mps = (sor_mps + soc_mps + som_mps) * mult_toggler(benediction, 1 - 0.15)

    consecration_mana = 320
    consecration_mps = consecration_mana / cons_cd * mult_toggler(not cons, 0)

    exorcism_mana = 180
    exorcism_mps = exorcism_mana / exorcism_cd * mult_toggler(not exorcism, 0)

    ds_mana = 0.12 * base_mana
    ds_mps = ds_mana / divine_storm_cd * mult_toggler(not ds, 0)

    holy_shock_mana = 225
    holy_shock_mps = holy_shock_mana / holy_shock_cd * mult_toggler(not shock, 0)

    divine_favor_mana = 0.04 * base_mana
    divine_favor_mps = divine_favor_mana / divine_favor_cd * mult_toggler(not divine_favor, 0)

    mana_loss_per_sec = (judge_mps + seal_mps + consecration_mps + exorcism_mps + ds_mps + holy_shock_mps +
                         divine_favor_mps)

    # mana gain
    bow_mana = 20 * mult_toggler(imp_bow, 1.2)
    bow_cd = 5
    bow_mps = bow_mana / bow_cd * mult_toggler(not bow, 0)

    guarded_mana = 0.05 * mana
    guarded_cd = 3
    guarded_mps = guarded_mana / guarded_cd * mult_toggler(not guarded, 0)

    wis_judge_mana = 50
    wis_judge_proc_chance = 0.5
    wis_judge_pps = wis_judge_proc_chance * 1 / melee_cd
    wis_judge_mps = wis_judge_mana * wis_judge_pps * mult_toggler(not wis_judge, 0)

    infusion_mana = holy_shock_mana
    infusion_pps = ((cd_ratio - 1) * spell_crit_c + 1) / divine_favor_cd
    infusion_mps = infusion_mana * infusion_pps

    mana_gain_per_sec = bow_mps + guarded_mps + wis_judge_mps + infusion_mps

    mana_net_flow = mana_gain_per_sec - mana_loss_per_sec

    if mana_net_flow < 0:
        time_until_oom = round(-mana / mana_net_flow, ndigits=1)
    else:
        time_until_oom = "Never"

    # threat per sec
    holy_mod = holy_threat_coefficient(imp_rf=imp_rf)
    non_holy_mod = 1.5

    tps = holy_dps * holy_mod + non_holy_dps * non_holy_mod + ds_hps * 0.5 * holy_mod

    print("---------------------------------------------------------")
    print(f"Build {name}")
    print(f"TPS: {round(tps, ndigits=1)}")
    print(f"DPS: {round(holy_dps + non_holy_dps, ndigits=1)}")
    print(f"{round(holy_dps / (non_holy_dps + holy_dps) * 100, ndigits=1)}% holy damage")
    print(f"Mana loss per sec: {-round(mana_net_flow, ndigits=1)}")
    print(f"Time until oom: {time_until_oom}")
    print(f"Melee crit chance: {round(melee_crit * 100, ndigits=1)}%")
    print()
    if Extended_Details:
        print("DPS Values")
        print(f"Melee: {round(melee_dps, ndigits=1)}")
        if cons:
            print(f"Consecration: {round(cons_dps, ndigits=1)}")
        if seal == "sor":
            if sor_three_dps > sor_five_dps:
                print(f"SoR 3: {round(sor_dps, ndigits=1)}")
            else:
                print(f"SoR 5: {round(sor_dps, ndigits=1)}")
        if seal == "soc":
            print(f"SoC: {round(soc_dps, ndigits=1)}")
        if seal == "som":
            print(f"SoM: {round(som_dps, ndigits=1)}")
        if shock:
            print(f"Holy Shock: {round(holy_shock_dps, ndigits=1)}")
        if exorcism:
            print(f"Exorcism: {round(exorcism_dps, ndigits=1)}")
        if ret_aura:
            print(f"Ret aura: {round(ret_aura_dps, ndigits=1)}")
        if ds:
            print(f"Divine Storm: {round(divine_storm_dps, ndigits=1)}")


# execution
threat_calculator(weapon_speed=Weapon_Speed, gear_agi=Gear_Agi, aow_judge_proc=AoW_Judge_Proc, wb=WB,
                  imp_sor=Improved_SoR, imp_rf=Improved_RF, imp_judge=Improved_Judge, art_of_war=Art_Of_War,
                  conviction_points=Conviction_Points, cons=Consecration, seal=Seal, gear_strength=Gear_Strength,
                  gear_ap=Gear_AP, kings=Kings, bom=BoM, battle_shout=Battle_Shout, divine_strength=Divine_Strength,
                  bonus_sp=Bonus_SP, sheath=Sheath, weapon_enchant_bonus=Weapon_Enchant_Bonus, weapon_min=Weapon_Min,
                  weapon_max=Weapon_Max, extra_crit=Bonus_Crit, precision=Precision, boss_dodge=Boss_Dodge,
                  boss_parry=Boss_Parry, armor_mitigation=Boss_Armor_Mitigation, ds=Divine_Storm,
                  name=Build_Name, spell_crit=Spell_Crit, ret_aura=Ret_Aura, boss_speed=Enemy_Speed, wf=WF,
                  deflection=Deflection, base_parry=Base_Parry, exorcism=Exorcism, shock=Holy_Shock,
                  crusader_judge=Judge_Of_Crusader, weapon_sp=Weapon_SP, weapon_str=Weapon_Strength,
                  benediction=Benediction, arcane=Arcane_Intellect, gear_int=Gear_Intellect, bow=BoW,
                  guarded=Guarded_By_Light, wis_judge=Judge_Of_Wisdom, holy_power=Holy_Power, imp_bow=Improved_BoW,
                  divine_favor=Divine_Favor, divine_int=Divine_Intellect,
                  handedness=Handedness, imp_crusader=Improved_Crusader, imp_ret=Improved_Ret_Aura,
                  two_hand_spec=Two_Hand_Spec, sanctity_aura=Sanctity_Aura, vengeance=Vengeance, racial=Racial_Bonus,
                  extra_wep_skill=Bonus_Skill, extra_hit=Bonus_Hit, horn=Horn, mark=MoW, infusion=Infusion, leader=LotP,
                  wep_agi=Weapon_Agility, wep_int=Weapon_Intellect)

#streamlit code

st.set_page_config(page_title='Paladin Threat and Damage Sim', layout='wide')

# ------------------------------------------------------------------
#streamlit app
hide_streamlit_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        </style>
        """

st.markdown(hide_streamlit_style,unsafe_allow_html=True)

top_row= st.container()
select_row= st.container()
big_row= st.container()
bottom_row= st.container()
fourth_row= st.container()
fifth_row= st.container()

with top_row:
    st.write('**Gear Stats**')
    #write map
    Total_Int = st.number_input('Total unbuffed int')
    Total_Str = st.number_input('Total unbuffed str')
    Total_Agi = st.number_input('Total unbuffed agi')
    Gear_AP = st.number_input('Total unbuffed AP from gear')
    Bonus_SP = st.number_input('Total unbuffed SP from gear')
    Bonus_Crit = st.number_input('Bonus crit from gear as decimal')
    Bonus_Skill = st.number_input('Bonus wep skill from gear')


with select_row:
    st.write('**Talent Toggles**')
# holy
    Improved_SoR = st.checkbox('Talent Selected')
    Improved_BoW = st.checkbox('Talent Selected')
    Divine_Strength = st.checkbox('Talent Selected')
    Divine_Intellect = st.checkbox('Talent Selected')
    Holy_Power = st.checkbox('Talent Selected')
# prot
    Precision = st.checkbox('Talent Selected')
    Improved_RF = st.checkbox('Talent Selected')
# ret
    Conviction_Points = st.number_input('Number of points, 0 to 5')
    Improved_Judge = st.checkbox('Talent Selected')
    Improved_Crusader = st.checkbox('Talent Selected')
    Deflection = st.checkbox('Talent Selected')
    Benediction = st.checkbox('Talent Selected')
    Improved_Ret_Aura = st.checkbox('Talent Selected')
    Two_Hand_Spec = st.checkbox('Talent Selected')
    Vengeance = st.checkbox('Talent Selected')

 
with big_row:
    st.write('**Ability Toggles**')
    Consecration = st.checkbox('Ability Usable')
    Seal = st.selectbox('Seal used', ("sor", "soc", "som")) # sor, soc or som
    Divine_Storm = st.checkbox('Ability Usable')
    Exorcism = st.checkbox('Ability Usable')
    Holy_Shock = st.checkbox('Ability Usable')
    Divine_Favor = st.checkbox('Ability Usable')
    Ret_Aura = st.checkbox('Ability Usable')

    Sheath = st.checkbox('Ability Usable')
    Infusion = st.checkbox('Ability Usable')

    Guarded_By_Light = st.checkbox('Ability Usable')
    Art_Of_War = st.checkbox('Ability Usable')

with bottom_row:
    st.write('**Weapon Info**')
    Weapon_Min = st.number_input('Weapon min')
    Weapon_Max = st.number_input('Weapon max')
    Weapon_Speed = st.number_input('Weapon speed')
    Weapon_Enchant_Bonus = st.number_input('Weapon enchant bonus')

    Weapon_Strength = st.input('Weapon added strength')
    Weapon_Intellect = st.input('Weapon added int')
    Weapon_Agility = st.input('Weapon added agi')
    Weapon_SP = st.input('Weapon added SP')
    Handedness = st.selectbox('One or two handed', (1,2))  # 1 or 2
    Racial_Bonus = st.checkbox('Racial bonus')



with fourth_row:
    # raid buffs
    Kings = st.input("kings")
    BoM = st.input('Blessing of might - exclusive with Horn')
    Horn = st.input('Horn of Lordaeron - exclusive with Might')
    Sanctity_Aura = st.input('Sanc aura')
    WB = st.input('World buff')
    Battle_Shout = st.input('Battle shout')
    WF = st.input('Windfury')
    Judge_Of_Crusader = st.input('Judgement of the Crusader')
    Arcane_Intellect = st.input('Arcane Intellect')
    BoW = st.input('Blessing of Wisdom')
    Judge_Of_Wisdom = st.input('Judgement of WIsdom')
    MoW = st.input('Mark of the Wild')
    LotP = st.input('Leader of the pack')

with fifth_row:
    st.write('Run sim')

    if st.button('Run sim'):
        result= threat_calculator(weapon_speed=Weapon_Speed, gear_agi=Gear_Agi, aow_judge_proc=AoW_Judge_Proc, wb=WB,
                  imp_sor=Improved_SoR, imp_rf=Improved_RF, imp_judge=Improved_Judge, art_of_war=Art_Of_War,
                  conviction_points=Conviction_Points, cons=Consecration, seal=Seal, gear_strength=Gear_Strength,
                  gear_ap=Gear_AP, kings=Kings, bom=BoM, battle_shout=Battle_Shout, divine_strength=Divine_Strength,
                  bonus_sp=Bonus_SP, sheath=Sheath, weapon_enchant_bonus=Weapon_Enchant_Bonus, weapon_min=Weapon_Min,
                  weapon_max=Weapon_Max, extra_crit=Bonus_Crit, precision=Precision, boss_dodge=Boss_Dodge,
                  boss_parry=Boss_Parry, armor_mitigation=Boss_Armor_Mitigation, ds=Divine_Storm,
                  name=Build_Name, spell_crit=Spell_Crit, ret_aura=Ret_Aura, boss_speed=Enemy_Speed, wf=WF,
                  deflection=Deflection, base_parry=Base_Parry, exorcism=Exorcism, shock=Holy_Shock,
                  crusader_judge=Judge_Of_Crusader, weapon_sp=Weapon_SP, weapon_str=Weapon_Strength,
                  benediction=Benediction, arcane=Arcane_Intellect, gear_int=Gear_Intellect, bow=BoW,
                  guarded=Guarded_By_Light, wis_judge=Judge_Of_Wisdom, holy_power=Holy_Power, imp_bow=Improved_BoW,
                  divine_favor=Divine_Favor, divine_int=Divine_Intellect,
                  handedness=Handedness, imp_crusader=Improved_Crusader, imp_ret=Improved_Ret_Aura,
                  two_hand_spec=Two_Hand_Spec, sanctity_aura=Sanctity_Aura, vengeance=Vengeance, racial=Racial_Bonus,
                  extra_wep_skill=Bonus_Skill, extra_hit=Bonus_Hit, horn=Horn, mark=MoW, infusion=Infusion, leader=LotP,
                  wep_agi=Weapon_Agility, wep_int=Weapon_Intellect)
        st.write('%s' % result)
