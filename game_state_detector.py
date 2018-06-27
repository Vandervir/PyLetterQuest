import time

from image_recognition import ImageRecognition
from text_recognition import TextRecognition


class GameStateDetector:
    STATE_PAUSE = 'pause'
    STATE_MONSTER_BATTLE = 'monster_battle'
    STATE_CHEST_MINIGAME = 'chest_minigame_letters'
    STATE_CHEST_MINIGAME_PRIZE = 'chest_minigame_prize'
    STATE_SHOP = 'shop'
    STATE_NONE = None

    def __init__(self):
        self.current_state = None
        self.tr = TextRecognition()
        self.ir = ImageRecognition()
        pass

    def get_game_state(self):
        if self._is_monster_battle_state():
            return self.STATE_MONSTER_BATTLE

        if self._is_shop_state():
            return self.STATE_SHOP

        if self._is_chest_minigame():
            return self.STATE_CHEST_MINIGAME

        if self._is_chest_minigame_reward():
            return self.STATE_CHEST_MINIGAME_PRIZE

        print('State not recognized')
        return self.STATE_NONE

    def _is_chest_minigame(self):
        resume = self._is_pause_resume_required()
        return self.ir.is_the_same_image((2282, 318, 2320, 356), 'img/chest_minigame.png', resume=resume,
                                         acceptable_ratio=0.7)

    def _is_chest_minigame_reward(self):
        resume = self._is_pause_resume_required()
        return self.ir.is_the_same_image((2282, 318, 2320, 356), 'img/chest_minigame_reward.png', resume=resume,
                                         acceptable_ratio=0.8)

    def _is_shop_state(self):
        resume = self._is_pause_resume_required()
        return self.ir.is_the_same_image((2417, 311, 2460, 354), 'img/show_state.png', resume=resume)

    def _is_monster_battle_state(self):
        resume = self._is_pause_resume_required()
        return self.ir.is_the_same_image((2093, 384, 2182, 473), 'img/shuffle_button.png', resume=resume)
        pass

    def _is_pause_resume_required(self):
        return self.ir.is_the_same_image((2418, 329, 2508, 367), 'img/resume_button.png', resume=False)

    def ms_has_correct_word(self):
        # Only in monster state
        region = (2461, 383, 2551, 473)
        resume = self._is_pause_resume_required()
        scythe_active = self.ir.get_image_similarity_score(region, 'img/ms_correct_word.png', resume=resume)
        scythe_inactive = self.ir.get_image_similarity_score(region, 'img/ms_correct_word_not.png')
        return scythe_active > scythe_inactive

    def ms_has_health_potion(self):
        # Only in monster state
        region = (2104, 498, 2125, 516)
        resume = self._is_pause_resume_required()
        active_potion = self.ir.get_image_similarity_score(region, 'img/ms_health_potion.png', resume=resume)
        inactive_potion = self.ir.get_image_similarity_score(region, 'img/ms_health_potion_none.png')
        return active_potion > inactive_potion

    def ms_has_purify_potion(self):
        # Only in monster state
        region = (2154, 498, 2175, 516)
        resume = self._is_pause_resume_required()
        active_potion = self.ir.get_image_similarity_score(region, 'img/ms_purify_potion.png', resume=resume)
        inactive_potion = self.ir.get_image_similarity_score(region, 'img/ms_purify_potion_none.png')
        return active_potion > inactive_potion
