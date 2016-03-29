/**
*******************************************************************************
* @file                  ERadParamIndexDsp.h
* @version               wn4_inc6#6.1
* @date                  27-APR-2007 09:47:20
* @author                ANKOKKON
*
* Item Specification     WCDMA:A33250.A-SRC
*
* Status                 DRAFT
*
* Original author        Sinikka Mikkola
*
* Copyright (c) Nokia 2006. All rights reserved.
******************************************************************************/

#ifndef _E_RAD_PARAM_INDEX_DSP_H
#define _E_RAD_PARAM_INDEX_DSP_H

typedef enum ERadParamIndexDsp
{
    ERadParamIndexDsp_HsupaEHichIOPinEnable                     = 0,
    /* [N/A] i32 scale:1 min:0 max:1, HSUPA I/O pin activation for HICH, 1 = Enable, 0 = Disable. */

    ERadParamIndexDsp_MaxAmount
    /* Keep this at last line */

}ERadParamIndexDsp;

#endif  /* _E_RAD_PARAM_INDEX_DSP_H*/

/******************************************************************************
* @enum ERadParamIndexDsp
* Development Workset : WCDMA:BS_ENV_WS
*
* Design Part         : WCDMA:BS_ENV.A;1
*
* Description         : Index enumeration for DSP related R&D parameter.
*                       Used as a parameter index when handling following
*                       messages in DSP subsystem:
*                       - GetRadParamsResp.h
*                       - SetRadParamsReq.h
*
* Reference           : HSUPA Element Feature Specification,
*                       location Doors
*
* @param ERadParamIndexDsp_HsupaEHichIOPinEnable :
*        [n/a] i32 scale:1 min:0 max:1, 1 = Enable, 0 = Disable.
*        HSUPA I/O pin activation for HICH
* @param ERadParamIndexDsp_MaxAmount :
*        Default value: N/A; Range: N/A; Step: N/A;
*        Maximum amount of R&D parameters/indices.
*        Keep this at last line.
*
* Additional Information : - 
*
* Definition Provided by : DSP / Sinikka Mikkola
* 
* Remember to put an empty line in the end of each definition file.
* Otherwise the compiler will generate a warning.
******************************************************************************/

