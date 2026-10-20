/**
 * Copyright(c) Live2D Inc. All rights reserved.
 *
 * Use of this source code is governed by the Live2D Open Software license
 * that can be found at https://www.live2d.com/eula/live2d-open-software-license-agreement_en.html.
 */


precision mediump float;
varying vec2 v_texCoord; //v2f.texcoord
varying vec4 v_clipPos;
uniform vec4 u_baseColor; //v2f.color
uniform vec4 u_channelFlag;
uniform sampler2D s_texture0; //_MainTex
uniform sampler2D s_texture1; // _ClippingMaskTex
uniform vec4 u_multiplyColor;
uniform vec4 u_screenColor;
uniform float u_bulge;

void main()
{
  vec2 uv = v_texCoord;

  vec2 center = uv - vec2(0.5);

  float dist = length(center);

  float strength = u_bulge * 0.45;

  float factor = 1.0 + strength * dist * dist;

  center *= factor;

  uv = center + vec2(0.5);

  uv = clamp(uv, 0.0, 1.0);

  vec4 texColor = texture2D(s_texture0, uv);
  texColor.rgb = texColor.rgb * u_multiplyColor.rgb;
  texColor.rgb = (texColor.rgb + u_screenColor.rgb * texColor.a) - (texColor.rgb * u_screenColor.rgb);
  vec4 col_formask = texColor * u_baseColor;
  vec4 clipMask = (1.0 - texture2D(s_texture1, v_clipPos.xy / v_clipPos.w)) * u_channelFlag;
  float maskVal = clipMask.r + clipMask.g + clipMask.b + clipMask.a;
  col_formask = col_formask * maskVal;
  gl_FragColor = col_formask;
}
