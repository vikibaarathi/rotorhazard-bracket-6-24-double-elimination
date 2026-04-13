"""
Double Elimination Bracket: 6-up, 24 pilots (MultiGP style)

Generates a 14-heat double elimination bracket for 24 pilots with 6 per heat.
Top 3 advance (winners path), bottom 3 drop (losers path) at each stage.

Bracket structure:
  R1 (Heats 1-4):     4 heats x 6 = 24 pilots seeded from qualifiers
  Losers R1 (5-6):    2 heats x 6 = bottom 3 from each R1 heat
  Winners R2 (7-8):   2 heats x 6 = top 3 from each R1 heat
  Losers R2 (9-10):   2 heats x 6 = LR1 survivors + WR2 drops
  Winners Semi (11):  1 heat x 6  = top 3 from each WR2 heat
  Losers R3 (12):     1 heat x 6  = top 3 from each LR2 heat
  Losers Semi (13):   1 heat x 6  = LR3 survivors + WS drops
  Final (14):         1 heat x 6  = WS top 3 + LS top 3

Eliminations (bottom 3 at each stage):
  19th-24th: Losers R1 (heats 5-6)
  13th-18th: Losers R2 (heats 9-10)
  10th-12th: Losers R3 (heat 12)
   7th-9th:  Losers Semi (heat 13)
   1st-6th:  Final (heat 14)
"""

import logging
from eventmanager import Evt
from HeatGenerator import HeatGenerator, HeatPlan, HeatPlanSlot, SeedMethod
from Results import RaceClassRankMethod
from RHUI import UIField, UIFieldType, UIFieldSelectOption

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Heat Generator
# ---------------------------------------------------------------------------

def bracket_de_6up_24(rhapi, generate_args=None):
    """Generate a 14-heat double elimination bracket for 24 pilots, 6 per heat."""

    seed_offset = 0
    if generate_args and 'seed_offset' in generate_args:
        seed_offset = max(int(generate_args['seed_offset']) - 1, 0)

    def S(rank):
        """Helper: create an INPUT seed slot with optional offset."""
        return HeatPlanSlot(SeedMethod.INPUT, rank + seed_offset)

    def H(position, heat_index):
        """Helper: create a HEAT_INDEX seed slot (position from a prior heat)."""
        return HeatPlanSlot(SeedMethod.HEAT_INDEX, position, heat_index)

    R = rhapi.__("Race")

    # -----------------------------------------------------------------------
    # Round 1: 4 heats, snake-seeded (MultiGP style)
    #
    # Snake seeding for 4 heats x 6 slots:
    #   Row 1 (L-R): H1=1,  H2=2,  H3=3,  H4=4
    #   Row 2 (R-L): H4=5,  H3=6,  H2=7,  H1=8
    #   Row 3 (L-R): H1=9,  H2=10, H3=11, H4=12
    #   Row 4 (R-L): H4=13, H3=14, H2=15, H1=16
    #   Row 5 (L-R): H1=17, H2=18, H3=19, H4=20
    #   Row 6 (R-L): H4=21, H3=22, H2=23, H1=24
    #
    # MultiGP convention: top seed in last heat
    #   H1: 3, 6, 11, 14, 19, 22
    #   H2: 2, 7, 10, 15, 18, 23
    #   H3: 4, 5, 12, 13, 20, 21
    #   H4: 1, 8, 9, 16, 17, 24
    # -----------------------------------------------------------------------

    heats = [
        # Index 0: Race 1
        HeatPlan(
            f"{R} 1",
            [S(3), S(6), S(11), S(14), S(19), S(22)]
        ),
        # Index 1: Race 2
        HeatPlan(
            f"{R} 2",
            [S(2), S(7), S(10), S(15), S(18), S(23)]
        ),
        # Index 2: Race 3
        HeatPlan(
            f"{R} 3",
            [S(4), S(5), S(12), S(13), S(20), S(21)]
        ),
        # Index 3: Race 4
        HeatPlan(
            f"{R} 4",
            [S(1), S(8), S(9), S(16), S(17), S(24)]
        ),

        # -------------------------------------------------------------------
        # Losers R1: bottom 3 from R1 heats
        # -------------------------------------------------------------------

        # Index 4: Race 5 — Losers R1a (bottom 3 from H1 + bottom 3 from H2)
        HeatPlan(
            f"{R} 5: {rhapi.__('Losers Round 1')}",
            [H(4, 0), H(5, 0), H(6, 0), H(4, 1), H(5, 1), H(6, 1)]
        ),
        # Index 5: Race 6 — Losers R1b (bottom 3 from H3 + bottom 3 from H4)
        HeatPlan(
            f"{R} 6: {rhapi.__('Losers Round 1')}",
            [H(4, 2), H(5, 2), H(6, 2), H(4, 3), H(5, 3), H(6, 3)]
        ),

        # -------------------------------------------------------------------
        # Winners R2: top 3 from R1 heats
        # -------------------------------------------------------------------

        # Index 6: Race 7 — Winners R2a (top 3 from H1 + top 3 from H2)
        HeatPlan(
            f"{R} 7: {rhapi.__('Winners Round 2')}",
            [H(1, 0), H(2, 0), H(3, 0), H(1, 1), H(2, 1), H(3, 1)]
        ),
        # Index 7: Race 8 — Winners R2b (top 3 from H3 + top 3 from H4)
        HeatPlan(
            f"{R} 8: {rhapi.__('Winners Round 2')}",
            [H(1, 2), H(2, 2), H(3, 2), H(1, 3), H(2, 3), H(3, 3)]
        ),

        # -------------------------------------------------------------------
        # Losers R2: LR1 survivors (top 3) + WR2 drops (bottom 3)
        # -------------------------------------------------------------------

        # Index 8: Race 9 — Losers R2a (top 3 from LR1a + bottom 3 from WR2a)
        HeatPlan(
            f"{R} 9: {rhapi.__('Losers Round 2')}",
            [H(1, 4), H(2, 4), H(3, 4), H(4, 6), H(5, 6), H(6, 6)]
        ),
        # Index 9: Race 10 — Losers R2b (top 3 from LR1b + bottom 3 from WR2b)
        HeatPlan(
            f"{R} 10: {rhapi.__('Losers Round 2')}",
            [H(1, 5), H(2, 5), H(3, 5), H(4, 7), H(5, 7), H(6, 7)]
        ),

        # -------------------------------------------------------------------
        # Winners Semifinal: top 3 from each WR2 heat
        # -------------------------------------------------------------------

        # Index 10: Race 11 — Winners Semi
        HeatPlan(
            f"{R} 11: {rhapi.__('Winners Semifinal')}",
            [H(1, 6), H(2, 6), H(3, 6), H(1, 7), H(2, 7), H(3, 7)]
        ),

        # -------------------------------------------------------------------
        # Losers R3: top 3 from each LR2 heat
        # -------------------------------------------------------------------

        # Index 11: Race 12 — Losers R3
        HeatPlan(
            f"{R} 12: {rhapi.__('Losers Round 3')}",
            [H(1, 8), H(2, 8), H(3, 8), H(1, 9), H(2, 9), H(3, 9)]
        ),

        # -------------------------------------------------------------------
        # Losers Semifinal: LR3 top 3 + Winners Semi bottom 3
        # -------------------------------------------------------------------

        # Index 12: Race 13 — Losers Semi
        HeatPlan(
            f"{R} 13: {rhapi.__('Losers Semifinal')}",
            [H(1, 11), H(2, 11), H(3, 11), H(4, 10), H(5, 10), H(6, 10)]
        ),

        # -------------------------------------------------------------------
        # Final: Winners Semi top 3 + Losers Semi top 3
        # -------------------------------------------------------------------

        # Index 13: Race 14 — Final
        HeatPlan(
            f"{R} 14: {rhapi.__('Final')}",
            [H(1, 10), H(2, 10), H(3, 10), H(1, 12), H(2, 12), H(3, 12)]
        ),
    ]

    return heats


# ---------------------------------------------------------------------------
# Class Ranking (resolves final positions from bracket results)
# ---------------------------------------------------------------------------

def rank_de_6up_24(rhapi, race_class, args):
    """
    Build a class leaderboard from the completed double-elimination bracket.

    Positions are determined by where each pilot was eliminated:
      1st-6th:   Final (heat index 13)
      7th-9th:   Losers Semi bottom 3 (heat index 12)
      10th-12th: Losers R3 bottom 3 (heat index 11)
      13th-15th: Losers R2a bottom 3 (heat index 8)
      16th-18th: Losers R2b bottom 3 (heat index 9)
      19th-21st: Losers R1a bottom 3 (heat index 4)
      22nd-24th: Losers R1b bottom 3 (heat index 5)
    """
    heats = rhapi.db.heats_by_class(race_class.id)

    if len(heats) < 14:
        logger.warning(f"DE Bracket 6x24: ranking requires 14 heats, found {len(heats)}")
        return None, None

    leaderboard = []
    position = 1

    def get_heat_results(heat_index):
        """Get primary leaderboard for a heat by its index in the class."""
        heat = heats[heat_index]
        races = rhapi.db.races_by_heat(heat.id)
        if not races:
            return []
        race_result = rhapi.db.race_results(races[0])
        if not race_result:
            return []
        return race_result[race_result['meta']['primary_leaderboard']]

    def add_pilots(heat_index, start_pos, end_pos, result_label):
        """Add pilots from a heat at positions start_pos..end_pos (1-based)."""
        nonlocal position
        results = get_heat_results(heat_index)
        for p in range(start_pos - 1, min(end_pos, len(results))):
            slot = results[p]
            leaderboard.append({
                'pilot_id': slot['pilot_id'],
                'callsign': slot['callsign'],
                'team_name': slot.get('team_name', ''),
                'position': position,
                'result': result_label.format(pos=p + 1),
            })
            position += 1

    # Build leaderboard from final backwards through elimination rounds
    add_pilots(13, 1, 6, "P{pos} in Final")
    add_pilots(12, 4, 6, "P{pos} in Losers Semifinal")
    add_pilots(11, 4, 6, "P{pos} in Losers Round 3")
    add_pilots(8,  4, 6, "P{pos} in Losers Round 2")
    add_pilots(9,  4, 6, "P{pos} in Losers Round 2")
    add_pilots(4,  4, 6, "P{pos} in Losers Round 1")
    add_pilots(5,  4, 6, "P{pos} in Losers Round 1")

    if not leaderboard:
        return None, None

    # Apply qualifier tiebreaker for pilots eliminated in the same round
    qualifier_class_id = args.get('qualifier_class')
    if qualifier_class_id:
        qualifier_class = rhapi.db.raceclass_by_id(qualifier_class_id)
        if qualifier_class:
            qual_results = rhapi.db.raceclass_results(qualifier_class)
            if qual_results and isinstance(qual_results, dict):
                qual_order = [r['pilot_id'] for r in qual_results['by_race_time']]

                tiebreak_ranges = [
                    (7, 9),    # Losers Semi bottom 3
                    (10, 12),  # Losers R3 bottom 3
                    (13, 15),  # Losers R2a bottom 3
                    (16, 18),  # Losers R2b bottom 3
                    (19, 21),  # Losers R1a bottom 3
                    (22, 24),  # Losers R1b bottom 3
                ]
                for start, end in tiebreak_ranges:
                    s = start - 1
                    e = end
                    if e <= len(leaderboard):
                        group = leaderboard[s:e]
                        group.sort(key=lambda x: qual_order.index(x['pilot_id'])
                                   if x['pilot_id'] in qual_order else 9999)
                        for i, entry in enumerate(group):
                            entry['position'] = start + i
                            leaderboard[s + i] = entry

    meta = {
        'method_label': "DE Bracket 6x24",
        'rank_fields': [
            {'name': 'result', 'label': 'Result'},
        ]
    }

    return leaderboard, meta


# ---------------------------------------------------------------------------
# Registration
# ---------------------------------------------------------------------------

class_rank_method = None

def register_heat_generator(args):
    """Register the heat generator with RotorHazard."""
    args['register_fn'](
        HeatGenerator(
            "DE Bracket, 6-up, 24-pilot (MultiGP)",
            bracket_de_6up_24,
            None,
            [
                UIField('seed_offset', "Seed from rank",
                        UIFieldType.BASIC_INT, value=1),
            ],
        )
    )

def register_class_rank(rhapi, args):
    """Register (or update) the class ranking method."""
    global class_rank_method

    classes = rhapi.db.raceclasses
    options = []
    for cls in classes:
        name = cls.name if cls.name else f"Class {cls.id}"
        options.append(UIFieldSelectOption(cls.id, name))

    default_class = options[0].value if options else 0

    if not class_rank_method:
        class_rank_method = RaceClassRankMethod(
            "DE Bracket 6x24",
            rank_de_6up_24,
            {
                'qualifier_class': default_class,
            },
            [
                UIField('qualifier_class',
                        "Qualifier class",
                        UIFieldType.SELECT,
                        options=options,
                        value=default_class,
                        desc="Class used for tiebreaker ordering"),
            ]
        )
        args['register_fn'](class_rank_method)
    else:
        class_rank_method.settings[0].options = options


def initialize(rhapi):
    """Plugin entry point — called by RotorHazard during server startup."""
    logger.info("DE Bracket 6x24: Initializing...")

    # Heat generator registration
    rhapi.events.on(Evt.HEAT_GENERATOR_INITIALIZE, register_heat_generator)

    # Class ranking registration (+ update on class changes)
    rhapi.events.on(Evt.CLASS_RANK_INITIALIZE,
                    lambda args: register_class_rank(rhapi, args))
    rhapi.events.on(Evt.CLASS_ADD,
                    lambda args: register_class_rank(rhapi, args))
    rhapi.events.on(Evt.CLASS_ALTER,
                    lambda args: register_class_rank(rhapi, args))
    rhapi.events.on(Evt.CLASS_DELETE,
                    lambda args: register_class_rank(rhapi, args))

    logger.info("DE Bracket 6x24: Initialization complete")
