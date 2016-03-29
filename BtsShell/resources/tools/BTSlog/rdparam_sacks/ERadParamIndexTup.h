/***********************************************************************
*                  Copyright (c) 2004 Nokia Networks
*                  All rights reserved
*
* FILENAME    : ERadParamIndexTup.h ver. ou_he#0.1
* DATE        : 18-MAR-2005 13:01:22
* AUTHOR      : LAKKISTO
* STATUS      : DRAFT
*
************************************************************************/

#ifndef _ERADPARAMINDEXTUP_H
#define _ERADPARAMINDEXTUP_H


typedef enum ERadParamIndexTup
{
    ERadParamIndexTup_HsdpaFcBuffThreshold          = 0,
    /* [bit/s] i32 scale:1 min:0 max:1000000           */

    ERadParamIndexTup_HsdpaFcBoost                  = 1,
    /* [bit/s] i32 scale:1000 min:-3600000 max:3600000 */

    ERadParamIndexTup_HsdpaFcPenalty                = 2,
    /* [bit/s] i32 scale:1000 min:-3600000 max:3600000 */

    ERadParamIndexTup_HsdpaFcZeroThreshold          = 3,
    /* [bit/s] i32 scale:1 min:0 max:1000000           */

    ERadParamIndexTup_HsdpaFcTpMultiplier           = 4,
    /* [n/a] i32 scale:0.05 min:0 max:2                */

    ERadParamIndexTup_HsdpaFcCreditDecreaseRatio    = 5,
    /* [n/a] i32 scale:0.1 min:1 max:10                */

    ERadParamIndexTup_HsdpaFcCreditIncreaseRatio    = 6,
    /* [n/a] i32 scale:0.1 min:1 max:10                */

    ERadParamIndexTup_HsdpaFcTimer                  = 7,
    /* [ms] i32 scale:10 min:10 max:1000               */

    ERadParamIndexTup_HsdpaFpInterval               = 8,
    /* [ms] i32 scale:10 min:10 max:2550               */

    ERadParamIndexTup_HsdpaFcTpMin                  = 9,
    /* [bit/s] i32 scale:1000 min:0 max:28800000       */

    ERadParamIndexTup_HsdpaFcTpMax                  = 10,
    /* [bit/s] i32 scale:1000 min:0 max:28800000       */

    ERadParamIndexTup_HsdpaFcTpEnable               = 11,
    /* [n/a] i32 scale:n/a min:off(0) max:on          */

    ERadParamIndexTup_HsdpaFcTpDefault              = 12,
    /* [bit/s] i32 scale:1000 min:0 max:28800000      */

    ERadParamIndexTup_HsdpaTFcInit                  = 13,
    /* [ms] i32 scale:10 min:10 max:5000              */

    ERadParamIndexTup_HsdpaTFcZero                  = 14,
    /* [ms] i32 scale:10 min:10 max:5000              */

    ERadParamIndexTup_TTDefaultLogLevel             = 15,
    /* [ELogType] u32 scale:n/a min:1 max:6 TUP TESTING */

    ERadParamIndexTup_TTPciPollMcu                  = 16,
    /* [ticks] u32 scale:n/a min:n/a max:n/a TUP TESTING */
    
    ERadParamIndexTup_TTSarPollMcu                  = 17,
    /* [ticks] u32 scale:n/a min:n/a max:n/a TUP TESTING */
    
    ERadParamIndexTup_TTAal2PollMcu                 = 18,
    /* [ticks] u32 scale:n/a min:n/a max:n/a TUP TESTING */
    
    ERadParamIndexTup_TTAal2ShaperPoll              = 19,
    /* [ticks] u32 scale:n/a min:n/a max:n/a TUP TESTING */

    ERadParamIndexTup_TTDscPollMcu                  = 20,
    /* [ticks] u32 scale:n/a min:n/a max:n/a TUP TESTING */

    ERadParamIndexTup_TTDscPollWsp                  = 21,
    /* [ticks] u32 scale:n/a min:n/a max:n/a TUP TESTING */

    ERadParamIndexTup_TTFifoPoll                    = 22,
    /* [ticks] u32 scale:n/a min:n/a max:n/a TUP TESTING */

    ERadParamIndexTup_TTOsPollMcu                   = 23,
    /* [ticks] u32 scale:n/a min:n/a max:n/a TUP TESTING */

    ERadParamIndexTup_TTOsPollWsp                   = 24,
    /* [ticks] u32 scale:n/a min:n/a max:n/a TUP TESTING */

    ERadParamIndexTup_TTSarPollLoopTime             = 25,
    /* [ticks] u32 scale:n/a min:n/a max:n/a TUP TESTING */

    ERadParamIndexTup_TTDscPollLoopTime             = 26,
    /* [ticks] u32 scale:n/a min:n/a max:n/a TUP TESTING */

    ERadParamIndexTup_TTMsgPollLoopTime             = 27,
    /* [ticks] u32 scale:n/a min:n/a max:n/a TUP TESTING */

    ERadParamIndexTup_TTBgFrameQueueNormal          = 28,
    /* [n/a] u32 scale:n/a min:n/a max:n/a TUP TESTING */

    ERadParamIndexTup_TTBgFrameQueueWarning	        = 29,
    /* [n/a] u32 scale:n/a min:n/a max:n/a TUP TESTING */

    ERadParamIndexTup_TTBgFrameQueueAlarm	        = 30,
    /* [n/a] u32 scale:n/a min:n/a max:n/a TUP TESTING */

    ERadParamIndexTup_TTBgTaskForceInterval         = 31,
    /* [ticks] u32 scale:n/a min:n/a max:n/a TUP TESTING */

    ERadParamIndexTup_TTNoAtmCac                    = 32,
    /* [n/a] u32 scale:n/a min:n/a max:n/a TUP TESTING */

    ERadParamIndexTup_TTNoAal2Cac	                = 33,
    /* [n/a] u32 scale:n/a min:n/a max:n/a TUP TESTING */

    ERadParamIndexTup_TTNoAAL2SLinkCheck	        = 34,
    /* [n/a] u32 scale:n/a min:n/a max:n/a TUP TESTING */

    ERadParamIndexTup_TTSaalCongestion10            = 35,
    /* [n/a] u32 scale:n/a min:n/a max:n/a TUP TESTING */

    ERadParamIndexTup_TTSaalHysteresis              = 36,
    /* [percent] u32 scale:n/a min:n/a max:n/a TUP TESTING */

    ERadParamIndexTup_TTSaalCongestionLevelFactor   = 37,
    /* [per mill] u32 scale:n/a min:n/a max:n/a TUP TESTING */

    ERadParamIndexTup_TTSaalCongestionFilterTime    = 38,
    /* [ms] u32 scale:n/a min:n/a max:n/a TUP TESTING */

    ERadParamIndexTup_TTLinkUpFilterTime             = 39,
    /* [ms] u32 scale:n/a min:n/a max:n/a TUP TESTING */

    ERadParamIndexTup_TTAalmAtmIsrLimit	             = 40,
    /* [n/a] u32 scale:n/a min:n/a max:n/a TUP TESTING */

    ERadParamIndexTup_TTAalmEthIsrLimit	             = 41,
    /* [n/a] u32 scale:n/a min:n/a max:n/a TUP TESTING */

    ERadParamIndexTup_TTDefaultLogMask	             = 42,
    /* [n/a] u32 scale:n/a min:n/a max:n/a TUP TESTING */

    ERadParamIndexTup_TTNoFpTaFilter	             = 43,
    /* [n/a] u32 scale:n/a min:n/a max:n/a TUP TESTING */

    ERadParamIndexTup_TTDebug1	                    = 44,
    /* [n/a] u32 scale:n/a min:n/a max:n/a TUP TESTING */

    ERadParamIndexTup_TTDebug2	                    = 45,
    /* [n/a] u32 scale:n/a min:n/a max:n/a TUP TESTING */

    ERadParamIndexTup_TTAal2CacMaxWeight	        = 46,
    /* [per mill] u32 scale:n/a min:n/a max:n/a TUP TESTING */

    ERadParamIndexTup_TTAal2CacAverageWeight	    = 47,
    /* [per mill] u32 scale:n/a min:n/a max:n/a TUP TESTING */

    ERadParamIndexTup_TTAal2CacConstantC	        = 48,
    /* [bit/s] u32 scale:n/a min:n/a max:n/a TUP TESTING */

    ERadParamIndexTup_TTResponseTimeoutInt	        = 49,
    /* [ms] u32 scale:n/a min:n/a max:n/a TUP TESTING */

    ERadParamIndexTup_TTResponseTimeoutExt	        = 50,
    /* [ms] u32 scale:n/a min:n/a max:n/a TUP TESTING */

    ERadParamIndexTup_TTAal2SigStopLevel	        = 51,
    /* [n/a] u32 scale:n/a min:n/a max:n/a TUP TESTING */

    ERadParamIndexTup_TTTimerTooLateLimitMcu	    = 52,
    /* [ticks] u32 scale:n/a min:n/a max:n/a TUP TESTING */

    ERadParamIndexTup_TTDlMsgTooLateLimitMcu	    = 53,
    /* [ticks] u32 scale:n/a min:n/a max:n/a TUP TESTING */

    ERadParamIndexTup_TTTimerTooLateLimitWsp	    = 54,
    /* [ticks] u32 scale:n/a min:n/a max:n/a TUP TESTING */

    ERadParamIndexTup_TTDlMsgTooLateLimitWsp	    = 55,
    /* [ticks] u32 scale:n/a min:n/a max:n/a TUP TESTING */

    ERadParamIndexTup_TTBgHsFpEstimatedTime	        = 56,
    /* [ticks] u32 scale:n/a min:n/a max:n/a TUP TESTING */


	ERadParamIndexTup_Stop
	/* Keep this at last line                         */

} ERadParamIndexTup;


#endif //_ERADPARAMINDEXTUP_H


/***********************************************************************
*
* SW Block            : Nora BTS / BS Env
*
* Development Workset : WCDMA:BS_ENV_WS
*
* Description : Index enumeration for TUP related R&D parameter.
*               Used as a parameter index when handling following
*               messages in TUP instance:
*               - GetRadParamsResp.h
*               - SetRadParamsReq.h
*               NOTE: parameters marked TUP TESTING should never
*               be changed except for TUP internal testing purposes!
*
* Reference   : BTS R&D Tools Interface Specification
*               - version 2.2, paragraph 4.1.5 (PI)
*               HSDPA EFS
*               - version 3.0, paragraph 3.13.2 (PI)
*
* Parameters  :
*
* Provider : TUP / J. Mäntysaari, K.Wikström
*
***********************************************************************/

