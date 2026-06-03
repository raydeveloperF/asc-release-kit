---
name: pixelmator-pxd-editor
description: Edit, create, modify, inspect, automate, or export Pixelmator Pro `.pxd` files. Use whenever Codex needs to work with PXD templates, App Store promotional PXD files, Pixelmator Pro mockups, layer replacement, text replacement, image replacement, PXD-to-PNG export, layer inspection, document resizing, masks, selections, or any user request that asks to edit a PXD file. This skill requires using only Pixelmator Pro's official AppleScript dictionary for editable PXD work and forbids direct PXD zip/SQLite/package mutation as the production path.
---

# Pixelmator PXD Editor

Use this skill for any task involving editable Pixelmator Pro `.pxd` files.

## Hard Rule

Edit PXD files only through Pixelmator Pro's official AppleScript dictionary. Use only the AppleScript commands and properties listed in this skill. If a needed action cannot be expressed with this allowed surface, stop and report the limitation instead of inventing another path.

Never use these as the production edit path:

- Unzipping or rezipping `.pxd` packages.
- Editing `metadata.info` SQLite data.
- Byte-patching layer BLOBs.
- Replacing `QuickLook` thumbnails.
- Replacing files under `data/*OriginalContentSource`.
- Recreating Apple device frames by hand when the template already contains one.
- Driving the UI with clicks, menu items, keyboard shortcuts, or clipboard state when an official AppleScript command/property exists.

Archive-level inspection is allowed only as read-only diagnostics after official AppleScript automation fails. Never ship a final PXD produced by package mutation unless the user explicitly asks for a forensic experiment.

## Safety Defaults

- Never modify the user's original PXD in place.
- Copy the PXD first, then open and edit only the copy.
- Disable Pixelmator Pro autosave while the script runs, then restore the previous value.
- Close only the document opened by the script, using `saving no` after exporting/saving the intended output.
- If Pixelmator Pro says the copied PXD is damaged or cannot be opened, stop and report that the template is invalid.
- Export a PNG preview after editing and inspect or report it before claiming success.
- For sensitive tasks, verify the original PXD timestamp did not change.

## Allowed Command Decision Table

Use this table as the main menu. Pick the row for the user's intent and use the exact command/property family named there.

| Want to do | Use this official AppleScript surface | Notes |
| --- | --- | --- |
| Open a copied PXD | `open POSIX file ...` | Always open the copy, never the original. |
| Create a new document/object/layer | `make` with `new`, `at`, `with data`, `with properties` | Use only when a blank/new layer is required. |
| Save edited PXD | `save as new document ... in ... as Pixelmator Pro` | Preferred PXD save path. |
| Export final file | `export ... to ... as PNG/JPEG/TIFF/WebP/etc.` | For App Store promo work, default to PNG. |
| Export compressed asset | `export optimized ... to ...` | Use only when the user asks for optimized export. |
| Export web asset | `export for web ... to ... as ... with properties ...` | Use for web-specific compression/scale/transparency. |
| Close after output | `close document saving no` | Close only the document this script opened. |
| Inspect document size | `width`, `height`, `resolution`, `bits per channel`, `color profile` | Read from `document`. |
| Change bit depth | `change color depth ... to ...` or `bits per channel` | Use only on the copied document. |
| Change color profile | `change color profile ... to ... mode ...` | Use when export/color profile is requested. |
| Find layers | `name of every text layer/image layer/group layer/shape layer` | Search nested groups; do not assume top-level. |
| Set active layer | `current layer` | Prefer direct layer references over current-selection workflows. |
| Select layers | `selected layers`, `select`, `select all layers` | Use only when a command requires selection. |
| Rename a layer | `name` property | Works on `layer`. |
| Show/hide a layer | `visible` property | Boolean. |
| Lock/unlock a layer | `locked` property | Boolean. |
| Set layer opacity | `opacity` property | Integer. |
| Move layer | `position` property or `bounds` property | Use exact coordinates. |
| Resize layer | `width`, `height`, or `bounds` property | Keep proportions manually if needed. |
| Rotate layer | `rotation` property | Degrees. This is 2D rotation, not true 3D perspective. |
| Change blend mode | `blend mode` property | Use official blend mode enumerators only. |
| Clip layer | `clipping mask` property | Boolean. |
| Replace iPhone screenshot/media | `replace image imageLayer with file scale mode scale to fill/scale to fit/original/stretch` | Preferred for templates because it preserves masks/effects/layout. |
| Add image content | `make image ... from file ...` or create `image layer` | For new assets, not placeholder replacement. |
| Change image layer source | `file` property on `image layer` or `replace image` | Prefer `replace image` for placeholders. |
| Preserve transparent pixels | `preserve transparency` property | Image layer property. |
| Keep layer proportions | `constrain proportions` property | Image/shape layer property. |
| Replace known text | `replace ... text ... with ... with properties ...` | Use for document-wide known placeholders. |
| Set headline text layer | `text content` on `text layer` | Preferred for named headline layers. |
| Style rich text | `color`, `font`, `size` on `rich text`/characters/words/paragraphs | Use only official text suite properties. |
| Align text layer | `horizontal alignment`, `vertical alignment` | Use text alignment enumerators. |
| Create rectangle | `make rectangle width ... height ... color ...` | For simple solid shape layers. |
| Create rounded rectangle | `make rounded rectangle width ... height ... corner radius ... color ...` | Use for simple UI/background shapes. |
| Group layers | `make group from ...` | Use when new generated layers need grouping. |
| Ungroup | `ungroup` | Use only on copied document/layers. |
| Duplicate object/layer | `duplicate ... to ... with properties ...` | Use for repeated decorations. |
| Delete copied-document layer/object | `delete` | Never delete from original document. |
| Merge specific layers | `merge layers ...` | Use only if user wants destructive flattening inside the copy. |
| Merge all layers | `merge all` | Avoid unless user asks for flattened output. |
| Merge visible layers | `merge visible` | Avoid unless user asks for flattened output. |
| Flatten document/layer stack | `flatten` | Avoid for editable PXD outputs; okay before raster-only export if requested. |
| Undo/redo script step | `undo`, `redo` | Recovery only; do not build primary workflow on undo. |
| Cut/copy/paste selection | `cut`, `copy`, `paste` | Use only when no direct layer command exists. Clipboard workflows are fallback. |
| Select all pixels | `select all` | Selection operation. |
| Clear selection | `deselect` | Selection operation. |
| Reselect previous selection | `reselect` | Selection operation. |
| Invert selection | `invert selection` | Selection operation. |
| Load layer/selection | `load selection ... mode ...` | Use official selection modes. |
| Select subject | `select subject ... smart refine ...` | ML-dependent; use only if user asks for subject selection. |
| Refine selection | `refine selection ... roundness ... softness ... expand ...` | Selection cleanup. |
| Smart-refine selection | `smart refine selection` | ML-dependent selection cleanup. |
| Select color range | `select color range ... color ... range ... mode ... smooth edges ...` | Use for color-based edits. |
| Draw rectangular selection | `draw selection ... bounds ... mode ...` | Coordinates required. |
| Draw elliptical selection | `draw elliptical selection ... bounds ... mode ...` | Coordinates required. |
| Convert selection to shape | `convert selection into shape` | Use when user asks to turn selection into editable shape. |
| Fill selection/layer | `fill ... with color ... preserve transparency ...` | Use official RGB color list. |
| Clear selected pixels | `clear` | Destructive inside copied document. |
| Pick pixel color | `pick color ... at ...` | Read diagnostic. |
| Crop document | `crop ... bounds ... delete mode ...` | Use when requested. |
| Resize image/document | `resize image ... width ... height ... resolution ... algorithm ...` | Changes image pixels. |
| Resize canvas | `resize canvas ... width ... height ... relative ... anchor position ...` | Changes canvas bounds. |
| Rotate canvas 180 | `rotate 180` | Whole image/document command. |
| Rotate canvas right | `rotate right` | Whole image/document command. |
| Rotate canvas left | `rotate left` | Whole image/document command. |
| Flip horizontally | `flip horizontally` | Whole selected target. |
| Flip vertically | `flip vertically` | Whole selected target. |
| Super-resolution upscale | `super resolution` | ML-dependent; use only when requested. |
| Trim canvas | `trim canvas ... mode ...` | Trim by transparency/color mode. |
| Reveal canvas | `reveal canvas` | Expands canvas to reveal off-canvas content. |
| Detect face | `detect face` | Read/ML utility; not a layout primitive. |
| Detect QR code | `detect QR code` | Read/utility. |
| Auto-enhance image | `enhance` | ML/auto adjustment; use only when requested. |
| Match colors to reference | `match colors ... to file ...` | Use when matching a reference image. |
| Auto white balance | `auto white balance` | Auto adjustment. |
| Auto light | `auto light` | Auto adjustment. |
| Auto color balance | `auto color balance` | Auto adjustment. |
| Auto hue/saturation | `auto hue and saturation` | Auto adjustment. |
| Auto levels contrast | `auto levels contrast` | Auto adjustment. |
| Auto levels color | `auto levels color` | Auto adjustment. |
| Auto curves contrast | `auto curves contrast` | Auto adjustment. |
| Auto curves color | `auto curves color` | Auto adjustment. |
| Denoise | `denoise ... intensity ...` | Use only when requested. |
| Deband | `deband` | Use only when requested. |
| Add mask from image | `mask ... from file ... scale mode ... mask mode ...` | Use official mask/scale modes. |
| Remove mask | `unmask` | Removes mask from target. |
| Remove background | `remove background` | ML-dependent; use only when requested. |
| Invert colors | `invert colors` | Destructive adjustment on target. |
| Decontaminate colors | `decontaminate colors` | Use after selections/background removal when requested. |
| Convert image layer into shape | `convert into shape` | Use only when requested. |
| Rasterize/convert into pixels | `convert into pixels` | Destructive; avoid unless required. |
| Apply color preset | `apply color adjustments preset name ...` | Use named Pixelmator preset. |
| Apply effects preset | `apply effects preset name ...` | Use named Pixelmator preset. |
| Reset target adjustments/effects | `reset` | Use only on copied document/layer. |
| Export LUT | `export as lut ... to file ...` | Use only when user requests LUT. |
| Make document from clipboard | `make document from clipboard` | Last-resort import path, not the normal PXD workflow. |

## Allowed Properties And Classes

Use these official properties for direct edits. Do not set undocumented keys.

- `application`: `autosave enabled`, `appearance`, `load hdr content`, `image opening workflow`, `sidecar enabled`, `sidecar location`, `build number`.
- `document`: `id`, `sidecar file`, `data reference`, `width`, `height`, `resolution`, `bits per channel`, `color profile`, `display hdr content`, `document info`, `current layer`, `selected layers`, `selection bounds`.
- `layer`: `id`, `index`, `data reference`, `name`, `opacity`, `visible`, `locked`, `selected`, `clipping mask`, `blend mode`, `width`, `height`, `position`, `bounds`, `rotation`, `color adjustments`, `styles`, `parent`, `layer mask`.
- `image layer`: `file`, `preserve transparency`, `constrain proportions`.
- `shape layer`: `constrain proportions`.
- `rounded rectangle shape layer`: `corner radius`.
- `polygon shape layer`: `sides`.
- `star shape layer`: `star points`, `star radius`.
- `text layer`: `text content`, `horizontal alignment`, `vertical alignment`.
- `rich text`, `character`, `word`, `paragraph`: `color`, `font`, `size`.
- `color adjustments`: `temperature`, `tint`, `hue`, `saturation`, `vibrance`, `exposure`, `highlights`, `shadows`, `brightness`, `contrast`, `black point`, `texture`, `clarity`, `black and white`, `sepia`, `invert`, `fade`, `vignette`, `vignette exposure`, `vignette black point`, `vignette softness`, `grain`, `grain size`, `sharpen`, `sharpen radius`, `custom lut`.
- `styles`: `fill color`, `fill opacity`, `fill blend mode`, `stroke width`, `stroke position`, `stroke type`, `stroke color`, `stroke opacity`, `shadow blur`, `shadow distance`, `shadow angle`, `shadow color`, `shadow opacity`, `inner shadow blur`, `inner shadow distance`, `inner shadow angle`, `inner shadow color`, `inner shadow opacity`, `inner shadow blend mode`.
- `document info`: metadata properties such as `author`, `caption`, `copyright notice`, `creation date`, `headline`, `keywords`, `title`, `location`, `altitude`.
- `effect`: `enabled`; specific effect properties include `radius`, `angle`, `position`, `amount`, `blur`, `transition`, `scale`, `rotation`, `color 1`, `color 2`, `width`, `sharpness`, `opacity`, `blend mode`, `fill color`, and image fill/pattern `image`.

## Allowed Enumerations

- Save formats for `save as new document`: `Pixelmator Pro`, `HEIC`, `JPEG`, `PNG`, `WebP`, `TIFF`, `SVG`, `GIF`, `PSD`.
- Export formats for `export`: `PNG`, `TIFF`, `JPEG`/`JPG`, `HEIC`, `GIF`, `JPEG2000`, `BMP`, `WebP`, `SVG`, `PDF`, `PSD`, `Pixelmator Pro`, `Motion`, `MP4`, `QuickTime Movie`, `Animated GIF`, `Animated PNG`, `OpenEXR`, `HDR JPEG`, `HDR HEIC`, `HDR AVIF`, `HDR PNG`.
- Export-for-web formats: `PNG`, `JPEG`, `GIF`, `SVG`, `WebP`.
- Scale modes: `original`, `stretch`, `scale to fill`, `scale to fit`.
- Selection modes: `new selection`, `add selection`, `subtract selection`, `intersect selection`.
- Mask modes: `reveal all`, `hide all`.
- Resize algorithms: `bilinear`, `lanczos`, `nearest`, `ml super resolution`.
- Canvas anchors: `top left`, `top center`, `top right`, `middle left`, `middle center`, `middle right`, `bottom left`, `bottom center`, `bottom right`.
- Trim modes: `transparency`, `top left color`, `bottom right color`.
- Color profile modes: `assign`, `match`.
- Text horizontal alignment: `left`, `center`, `right`, `justify`.
- Text vertical alignment: `top`, `center`, `bottom`.
- Stroke position: `inside`, `center`, `outside`.
- Stroke type: `line`, `dash`, `dot`.
- Blend modes: `normal`, `darken`, `multiply`, `color burn`, `linear burn`, `darker color`, `lighten`, `screen`, `color dodge`, `linear dodge`, `lighter color`, `overlay`, `soft light`, `hard light`, `vivid light`, `linear light`, `pin light`, `hard mix`, `difference`, `exclusion`, `subtract`, `divide`, `hue blend mode`, `saturation blend mode`, `color blend mode`, `luminosity`, `pass through`, `behind blend mode`.

## Layer Handling

Do not assume placeholders are top-level. Many Pixelmator templates nest the device screen inside a device group.

Example verified path:

`group layer "iPhone 16 Pro"` -> `image layer "Media Placeholder: Replace With Your Media"`

Inspect first:

```applescript
tell application "Pixelmator Pro"
  set d to open (POSIX file "/path/to/copied-template.pxd")
  tell d
    set reportText to "top text: " & ((name of every text layer) as text) & linefeed
    set reportText to reportText & "top images: " & ((name of every image layer) as text) & linefeed
    set reportText to reportText & "top groups: " & ((name of every group layer) as text)
    return reportText
  end tell
end tell
```

If nested groups are likely, inspect by known group names first, then recurse manually through `group layer` references. Prefer named placeholders over selected/current layers.

## Safe Edit Pattern

Use this shape for normal PXD edits:

```applescript
set copiedPXD to POSIX file "/path/to/copied-template.pxd"
set screenshotFile to POSIX file "/path/to/screenshot.png"
set outputPXD to POSIX file "/path/to/output/page1.pxd"
set outputPNG to POSIX file "/path/to/output/page1.png"
set headlineText to "A quiet place for memories"

tell application "Pixelmator Pro"
  activate
  set oldAutosave to autosave enabled
  set autosave enabled to false

  set demoDoc to open copiedPXD
  delay 1

  tell demoDoc
    try
      set text content of text layer "Headline" to headlineText
    end try

    set phoneGroup to group layer "iPhone 16 Pro"
    set screenLayer to image layer "Media Placeholder: Replace With Your Media" of phoneGroup
    replace image screenLayer with screenshotFile scale mode scale to fill

    save as new document it in outputPXD as Pixelmator Pro
    export it to outputPNG as PNG
  end tell

  close demoDoc saving no
  set autosave enabled to oldAutosave
end tell
```

If a script fails after changing `autosave enabled`, restore it before stopping. If the document is still open, close only the document this script opened.

## Forbidden Fallbacks

Do not use these unless the user explicitly asks for an experiment and accepts that the output may not be a valid editable PXD:

- Direct package mutation.
- SQLite metadata writes.
- Binary/BLOB edits.
- QuickLook thumbnail swaps.
- Raw replacement of embedded source files.
- Manually drawn Apple device frames when a template frame exists.
- GUI automation in place of available AppleScript commands.

## What To Say Back

Report:

- The edited `.pxd` path.
- The exported `.png` path.
- Whether the original PXD was left untouched.
- The AppleScript commands used.
- Any layer names or operations that could not be found/supported.
