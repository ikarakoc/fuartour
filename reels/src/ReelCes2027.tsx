// Per-video composition for edit/promo-ces-2027: the kit's scenes and end card over full-frame background images.
// The kit draws full scenes on an opaque field; here the field is made transparent (scoped CSS) so the images show through
// under a flat darkening in the brand's primary color.
import React from "react";
import { AbsoluteFill, Easing, Img, interpolate, staticFile, useCurrentFrame } from "remotion";
import { EndCard, KIT_FPS, ReelKitProps } from "./ReelKit";
import { alpha, styleLook, useLookFonts } from "./kit/brand";
import { SceneLayer } from "./kit/scenes";

// background image per span of the video (seconds)
const BG: { file: string; from: number }[] = [
  { file: "promo-ces-2027/bg1.jpg", from: 0 },
  { file: "promo-ces-2027/bg2.jpg", from: 3.2 },
  { file: "promo-ces-2027/bg3.jpg", from: 7.2 },
  { file: "promo-ces-2027/bg4.jpg", from: 9.9 },
  { file: "promo-ces-2027/bg5.jpg", from: 12.7 },
];
const FADE = 8; // frames
const DIM = 0.66;

const hexToRgb = (hex: string) => {
  const n = parseInt(hex.replace("#", ""), 16);
  return `rgb(${(n >> 16) & 255}, ${(n >> 8) & 255}, ${n & 255})`;
};

export const ReelCes2027: React.FC<ReelKitProps> = (p) => {
  const frame = useCurrentFrame();
  const look = styleLook(p.brand, p.style);
  const fonts = useLookFonts(look);
  const end = Math.round(p.captions.duration * KIT_FPS) + 78;
  const field = hexToRgb(look.field ?? p.brand.colors.primary);
  return (
    <AbsoluteFill style={{ backgroundColor: p.brand.colors.primary }}>
      {BG.map((b, i) => {
        const a = Math.round(b.from * KIT_FPS);
        const z = i + 1 < BG.length ? Math.round(BG[i + 1].from * KIT_FPS) + FADE : end;
        if (frame < a || frame >= z) return null;
        const op = i === 0 ? 1 : interpolate(frame, [a, a + FADE], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
        const s = interpolate(frame, [a, z], [1.04, 1.14], { easing: Easing.out(Easing.quad) });
        return (
          <AbsoluteFill key={b.file} style={{ opacity: op }}>
            <Img src={staticFile(b.file)} style={{ width: "100%", height: "100%", objectFit: "cover", transform: `scale(${s})` }} />
          </AbsoluteFill>
        );
      })}
      <AbsoluteFill style={{ backgroundColor: alpha(p.brand.colors.primary, DIM) }} />
      <style>{`.ces-scenes div[style*="background-color: ${field}"] { background-color: transparent !important; }`}</style>
      <AbsoluteFill className="ces-scenes">
        <SceneLayer scenes={p.scenes} brand={p.brand} look={look} words={p.captions.words} scenesOnly sceneTone={p.sceneTone} framed={null} />
      </AbsoluteFill>
      <EndCard p={p} look={look} fonts={fonts} />
    </AbsoluteFill>
  );
};
