# msv
memory struct viewer

önce pycparser ı indirin:
pip install pycparser

targetstruct.h ve stw.py aynı dizinde olsun
memory de görmek istediğiniz struct u targetstruct.h dosyasına atın:
```c
struct VampireSurvivors_Objects_Characters_CharacterController_Fields {
	struct ArcadeSprite_Fields filler;
	int32_t _PlayerIndex;
	struct UnityEngine_SpriteRenderer_o* _CharacterRenderer;
	struct UnityEngine_SpriteRenderer_o* _DeathNoHurtRenderer;
	struct Zenject_SignalBus_o* _signalBus;
	struct VampireSurvivors_Objects_PlayerOptions_o* _playerOptions;
	struct VampireSurvivors_Framework_GameManager_o* _gameManager;
	struct Rewired_Player_o* _player;
	struct UnityEngine_Transform_o* _cachedTransform;
	struct VampireSurvivors_Objects_CharacterWeaponsManager_o* _weaponsManager;
	struct VampireSurvivors_Objects_CharacterAccessoriesManager_o* _accessoriesManager;
	struct VampireSurvivors_Graphics_SpriteAnimation_o* _spriteAnimation;
	struct UnityEngine_ParticleSystem_o* _damageVfx;
	struct VampireSurvivors_Graphics_SpriteTrail_o* _spriteTrail;
	struct VampireSurvivors_UI_Player_HealthBar_o* _healthBar;
	struct VampireSurvivors_Data_DataManager_o* _dataManager;
	struct Newtonsoft_Json_Linq_JObject_o* _currentJsonData;
	struct VampireSurvivors_Data_Characters_CharacterData_o* _currentCharacterData;
	struct VampireSurvivors_Data_Characters_CharacterData_o* _currentSkinData;
	struct VampireSurvivors_Data_Characters_CharacterData_o* _levelZeroCharacterData;
	struct System_Collections_Generic_List_WeaponType__o* _weaponSelection;
	int32_t _startingWeaponType;
	int32_t _characterType;
	struct VampireSurvivors_Framework_TimerSystem_Timer_o* _regenTimer;
	struct VampireSurvivors_Framework_TimerSystem_Timer_o* _blinkTimeoutTimer;
	bool _receivingDamage;
	float _invincibilityTimer;
	bool _hasWalkingAnimation;
	struct VampireSurvivors_Framework_PhaserTweens_MultiTargetTween_o* _wiggleTween;
	struct UnityEngine_Vector2_o _currentDirection;
	struct UnityEngine_Vector2_o _currentDirectionRaw;
	struct UnityEngine_Vector2_o _lastMovementDirection;
	struct UnityEngine_MaterialPropertyBlock_o* _propBlock;
	struct ArcadeBodyBounds_o* _worldBoxCollider;
	struct ArcadeBodyBounds_o* _coopMovementBoxCollider;
	struct VampireSurvivors_Objects_ModifierStats_o* _onEveryLevelUp;
	struct VampireSurvivors_Objects_PlayerModifierStats_o* _playerStats;
	float _slowMultiplier;
	bool _isSlow;
	float _currentHp;
	int32_t _level;
	float _walked;
	struct UnityEngine_Vector2_o _lastFacingDirection;
	float _xp;
	bool _isAnimForced;
	bool _canFlip;
	bool _isFlipped;
	float _shieldInvulTime;
	struct VampireSurvivors_Objects_MagnetZone_o* _magnet;
	struct VampireSurvivors_Objects_SineBonus_o* _sineSpeed;
	struct VampireSurvivors_Objects_SineBonus_o* _sineCooldown;
	struct VampireSurvivors_Objects_SineBonus_o* _sineArea;
	struct VampireSurvivors_Objects_SineBonus_o* _sineDuration;
	struct VampireSurvivors_Objects_SineBonus_o* _sineMight;
	float _slowTime;
	float _gFeverMul;
	struct System_Action_float__o* _onHpRecoveryCallback;
	bool _isInFinalStage;
	bool _isDead;
	bool _isInvul;
	bool _isLastBreathEnabled;
	bool _hasLastBreath;
	struct System_Action_o* _onLastBreath;
	int32_t _maxWeaponCount;
	int32_t _maxAccessoryCount;
	struct VampireSurvivors_UI_Player_MultiplayerRevivalUI_o* _multiplayerRevivalUI;
	struct UnityEngine_SpriteRenderer_o* _multiplayerIndicator;
	struct VampireSurvivors_Objects_Characters_SpriteOutlinerControl_o* _multiplayerOutliner;
	float _multiplayerRevivalProportion;
	int32_t _revivalJuiceThisFrame;
	struct VampireSurvivors_Framework_TimerSystem_Timer_o* _multiplayerChompTimer;
	struct VampireSurvivors_Framework_TimerSystem_Timer_o* _multiplayerIndicatorTimer;
	struct VampireSurvivors_Framework_TimerSystem_Timer_o* _multiplayerDecompositionTimer;
	struct UnityEngine_Transform_o* _multiplayerCameraTargetTransform;
	struct VampireSurvivors_Framework_TimerSystem_Timer_o* _deathConsequenceTimer;
	struct VampireSurvivors_Framework_TimerSystem_Timer_o* _multiplayerReviveShake1;
	struct VampireSurvivors_Framework_TimerSystem_Timer_o* _multiplayerReviveShake2;
	bool _multiplayerRevivalAllowed;
	bool _AlwaysCoinBag_k__BackingField;
	bool _AlwaysRoast_k__BackingField;
	bool _AlwaysRandomLimitBreak_k__BackingField;
};
```
Not:
struct ın içinde başka struct lar varsa onları da atın. cpp header larının özelliği olan inherit struct pycparser tarafından desteklenmediği için inherit edilen struct un size ı kadar boyutta filler bir struct oluşturup esas struct un içine atın ki sıra kaymasın(Attığım targetstruct.h dosyasında bunun örnekleri var)
<img width="1124" height="210" alt="image" src="https://github.com/user-attachments/assets/9d6d1ed5-d271-487c-91b6-469ddee16a40" />

- hedef process id: pid/p
- hedef process deki struct adresi: address/a
- hedef struct ismi: struct_name/s

`python stv.py -p=29132 -a=0000022FB961D650 -s=VampireSurvivors_Objects_Characters_CharacterController_Fields`
<img width="1492" height="681" alt="image" src="https://github.com/user-attachments/assets/88236bf7-30d5-4d76-aa7d-bcf683820b31" />
