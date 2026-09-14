#!/usr/bin/env python3
"""
Script to translate English markdown files to Vietnamese.
Keeps code blocks, URLs, frontmatter, and technical terms intact.
"""

import re
import os

# Technical terms to keep in English
TECH_TERMS = {
    'class', 'promise', 'callback', 'DOM', 'fetch', 'constructor', 'prototype',
    'inheritance', 'static', 'private', 'protected', 'mixin', 'try-catch', 'async/await',
    'generator', 'module', 'export/import', 'event', 'bubbling', 'capturing', 'delegation',
    'mouse', 'keyboard', 'drag', 'drop', 'pointer', 'focus', 'blur', 'form', 'submit',
    'mutation', 'observer', 'selection', 'range', 'event loop', 'microtask', 'macrotask',
    'popup', 'window', 'cross-window', 'clickjacking', 'ArrayBuffer', 'TextDecoder',
    'TextEncoder', 'Blob', 'File', 'FileReader', 'Symbol', 'extend', 'extends', 'super',
    'this', 'new', 'instanceof', 'interface', 'property', 'method', 'function', 'object',
    'array', 'string', 'number', 'boolean', 'null', 'undefined', 'NaN', 'Infinity',
    'Error', 'SyntaxError', 'ReferenceError', 'TypeError', 'RangeError', 'URIError',
    'JSON', 'parse', 'stringify', 'setTimeout', 'setInterval', 'clearTimeout',
    'clearInterval', 'alert', 'prompt', 'confirm', 'console', 'log', 'debug',
    'element', 'node', 'document', 'window', 'body', 'head', 'style', 'classList',
    'className', 'innerHTML', 'outerHTML', 'textContent', 'value', 'checked', 'disabled',
    'selected', 'readonly', 'required', 'placeholder', 'autofocus', 'tabindex',
    'event', 'target', 'currentTarget', 'preventDefault', 'stopPropagation',
    'addEventListener', 'removeEventListener', 'dispatchEvent', 'CustomEvent',
    'MouseEvent', 'KeyboardEvent', 'FocusEvent', 'InputEvent', 'ChangeEvent',
    'SubmitEvent', 'ClipboardEvent', 'DragEvent', 'TouchEvent', 'PointerEvent',
    'WheelEvent', 'AnimationEvent', 'TransitionEvent', 'load', 'unload', 'beforeunload',
    'DOMContentLoaded', 'readystatechange', 'hashchange', 'popstate', 'storage',
    'localStorage', 'sessionStorage', 'cookie', 'indexedDB', 'WebSocket', 'Worker',
    'SharedWorker', 'ServiceWorker', 'fetch', 'XMLHttpRequest', 'FormData',
    'URLSearchParams', 'Headers', 'Request', 'Response', 'Blob', 'File', 'FileReader',
    'ArrayBuffer', 'DataView', 'Uint8Array', 'Int8Array', 'Uint16Array', 'Int16Array',
    'Uint32Array', 'Int32Array', 'Float32Array', 'Float64Array', 'Uint8ClampedArray',
    'BigInt64Array', 'BigUint64Array', 'TextDecoder', 'TextEncoder', 'URL',
    'URLPattern', 'RegExp', 'Map', 'Set', 'WeakMap', 'WeakSet', 'Promise', 'Proxy',
    'Reflect', 'Symbol', 'Iterator', 'AsyncIterator', 'Generator', 'AsyncGenerator',
    'await', 'async', 'yield', 'yield*', 'throw', 'catch', 'finally', 'try',
    'import', 'export', 'default', 'from', 'as', 'namespace', 'module', 'dynamic import',
    'import()', 'import.meta', 'globalThis', 'global', 'self', 'window', 'frames',
    'parent', 'top', 'opener', 'closed', 'location', 'navigator', 'screen', 'history',
    'document', 'console', 'Math', 'Date', 'Number', 'String', 'Array', 'Object',
    'Function', 'Boolean', 'RegExp', 'Error', 'EvalError', 'RangeError', 'ReferenceError',
    'SyntaxError', 'TypeError', 'URIError', 'AggregateError', 'Intl', 'JSON', 'Atomics',
    'WebAssembly', 'SharedArrayBuffer', 'Atomics', 'DataView', 'FinalizationRegistry',
    'WeakRef', 'structuredClone', 'transferable', 'postMessage', 'MessageChannel',
    'MessagePort', 'BroadcastChannel', 'EventSource', 'ServerSentEvent',
    'RequestIdleCallback', 'cancelIdleCallback', 'requestAnimationFrame', 'cancelAnimationFrame',
    'IntersectionObserver', 'ResizeObserver', 'MutationObserver', 'PerformanceObserver',
    'ReportingObserver', 'ContentVisibility', 'AutoSizing', 'Containment', 'LayoutShift',
    'CLS', 'LCP', 'FID', 'TTFB', 'FCP', 'TBT', 'SI', 'Performance', 'PerformanceEntry',
    'PerformanceMark', 'PerformanceMeasure', 'PerformanceNavigation', 'PerformanceResourceTiming',
    'PerformanceTiming', 'PerformanceNavigationTiming', 'PerformancePaintTiming',
    'PerformanceObserverEntryList', 'PerformanceObserverEntryType', 'PerformanceLongTaskTiming',
    'LayoutShiftAttribution', 'LayoutShift', 'Element', 'HTMLElement', 'HTMLDocument',
    'HTMLCollection', 'HTMLFormElement', 'HTMLInputElement', 'HTMLSelectElement',
    'HTMLTextAreaElement', 'HTMLButtonElement', 'HTMLAnchorElement', 'HTMLImageElement',
    'HTMLCanvasElement', 'HTMLVideoElement', 'HTMLAudioElement', 'HTMLSourceElement',
    'HTMLTrackElement', 'HTMLScriptElement', 'HTMLStyleElement', 'HTMLLinkElement',
    'HTMLMetaElement', 'HTMLBaseElement', 'HTMLTitleElement', 'HTMLHeadElement',
    'HTMLBodyElement', 'HTMLHtmlElement', 'HTMLDivElement', 'HTMLSpanElement',
    'HTMLParagraphElement', 'HTMLHeadingElement', 'HTMLUListElement', 'HTMLOListElement',
    'HTMLLIElement', 'HTMLTableElement', 'HTMLTableRowElement', 'HTMLTableCellElement',
    'HTMLTableSectionElement', 'HTMLTableCaptionElement', 'HTMLModElement',
    'HTMLQuoteElement', 'HTMLPreElement', 'HTMLHRElement', 'HTMLBRElement',
    'HTMLDialogElement', 'HTMLDetailsElement', 'HTMLSummaryElement', 'HTMLDataElement',
    'HTMLTimeElement', 'HTMLSlotElement', 'HTMLTemplateElement', 'ShadowRoot',
    'Slot', 'CustomElementRegistry', 'HTMLElement', 'ElementInternals',
    'CSSStyleDeclaration', 'CSSRule', 'CSSStyleSheet', 'CSSGroupingRule',
    'CSSMediaRule', 'CSSSupportsRule', 'CSSNamespaceRule', 'CSSPageRule',
    'CSSFontFaceRule', 'CSSKeyframesRule', 'CSSKeyframeRule', 'CSSCounterStyleRule',
    'CSSFontFeatureValuesRule', 'CSSPropertyRule', 'CSSImportRule', 'CSSCharsetRule',
    'CSSConditionRule', 'CSSConditionRule', 'CSSUnknownRule', 'CSSStyleRule',
    'CSSStyleSheet', 'CSSRuleList', 'CSSMediaList', 'CSSPageRule', 'CSSFontFaceRule',
    'CSSKeyframesRule', 'CSSKeyframeRule', 'CSSCounterStyleRule', 'CSSFontFeatureValuesRule',
    'CSSPropertyRule', 'CSSImportRule', 'CSSCharsetRule', 'CSSConditionRule',
    'CSSStyleRule', 'CSSStyleDeclaration', 'CSSValue', 'CSSPrimitiveValue',
    'CSSValueList', 'RGBColor', 'Rect', 'Counter', 'ElementCSSInlineStyle',
    'LinkStyle', 'StyleSheet', 'StyleSheetList', 'MediaList', 'DOMImplementation',
    'DocumentType', 'Entity', 'Notation', 'ProcessingInstruction', 'CDATASection',
    'Comment', 'Text', 'Attr', 'NamedNodeMap', 'NodeList', 'HTMLCollection',
    'DocumentFragment', 'Document', 'Window', 'Location', 'History', 'Navigator',
    'Screen', 'BarProp', 'ClientRect', 'DOMRect', 'DOMRectList', 'DOMRectReadOnly',
    'DOMMatrix', 'DOMMatrixReadOnly', 'DOMPoint', 'DOMPointReadOnly', 'DOMQuad',
    'GeometryUtils', 'ScrollOptions', 'ScrollToOptions', 'ScrollIntoViewOptions',
    'ScrollLogicalPosition', 'ScrollBehavior', 'ElementScrollOptions',
    'Event', 'CustomEvent', 'EventTarget', 'EventListener', 'EventListenerOptions',
    'AddEventListenerOptions', 'RemoveEventListenerOptions', 'EventListenerOrEventListenerObject',
    'Animation', 'AnimationEffect', 'KeyframeEffect', 'AnimationTimeline',
    'DocumentTimeline', 'AnimationPlaybackEvent', 'AnimationEvent', 'TransitionEvent',
    'CSSTransition', 'CSSAnimation', 'AnimationEffectTiming', 'AnimationEffectTimingReadOnly',
    'KeyframeAnimationOptions', 'AnimationOptions', 'EffectTiming', 'OptionalEffectTiming',
    'ComputedKeyframe', 'Keyframe', 'AnimationFillMode', 'AnimationDirection',
    'AnimationPlayState', 'PlaybackDirection', 'FillMode', 'SingleAnimationFillMode',
    'IterationCompositeOperation', 'CompositeOperation', 'CompositeOperationOrAuto',
    'ScrollTimeline', 'ViewTimeline', 'AnimationTimeline', 'DocumentTimeline',
    'WorkletAnimationEffect', 'WorkletAnimationEffectOptions', 'Worklet',
    'AudioWorklet', 'AudioWorkletNode', 'AudioWorkletProcessor', 'AudioWorkletGlobalScope',
    'AudioParam', 'AudioParamMap', 'AudioParamDescriptor', 'AudioWorkletProcessor',
    'AudioWorkletNodeOptions', 'AudioWorkletProcessorOptions', 'AudioWorkletGlobalScopeOptions',
    'OfflineAudioContext', 'AudioContext', 'AudioContextOptions', 'AudioContextLatencyCategory',
    'AudioListener', 'AudioDestinationNode', 'AudioNode', 'AudioParam', 'AudioParamMap',
    'AudioScheduledSourceNode', 'OscillatorNode', 'OscillatorType', 'GainNode',
    'DelayNode', 'BiquadFilterNode', 'BiquadFilterType', 'WaveShaperNode',
    'PeriodicWave', 'PeriodicWaveConstraints', 'ConstantSourceNode', 'MediaElementAudioSourceNode',
    'MediaStreamAudioSourceNode', 'MediaStreamAudioDestinationNode', 'MediaStreamTrackAudioSourceNode',
    'ScriptProcessorNode', 'AudioProcessingEvent', 'AudioBuffer', 'AudioBufferOptions',
    'AudioBufferSourceNode', 'AudioBufferSourceOptions', 'ConvolverNode',
    'ChannelMergerNode', 'ChannelSplitterNode', 'DynamicsCompressorNode',
    'StereoPannerNode', 'PannerNode', 'PanningModelType', 'DistanceModelType',
    'IIRFilterNode', 'IIRFilterOptions', 'AnalyserNode', 'AnalyserOptions',
    'MediaStream', 'MediaStreamTrack', 'MediaStreamTrackEvent', 'MediaStreamConstraints',
    'MediaTrackConstraints', 'MediaTrackSettings', 'MediaTrackCapabilities',
    'MediaTrackSupportedConstraints', 'MediaStreamTrackGenerator', 'MediaStreamTrackProcessor',
    'MediaStreamTrackAudioSource', 'MediaStreamTrackVideoSource', 'MediaStreamTrackProcessorOptions',
    'MediaStreamTrackGeneratorOptions', 'MediaStreamTrackEventInit', 'MediaStreamOptions',
    'MediaStreamTrackOptions', 'MediaStreamConstraints', 'MediaTrackConstraints',
    'MediaTrackSettings', 'MediaTrackCapabilities', 'MediaTrackSupportedConstraints',
    'ConstrainBoolean', 'ConstrainLong', 'ConstrainDouble', 'ConstrainDOMString',
    'ConstrainBooleanParameters', 'ConstrainLongRange', 'ConstrainDoubleRange',
    'ConstrainDOMStringParameters', 'DoubleRange', 'LongRange', 'MediaStreamError',
    'MediaStreamErrorEvent', 'OverconstrainedError', 'MediaDevices', 'MediaDeviceInfo',
    'MediaDeviceKind', 'EnumerateDevicesOptions', 'MediaKeySystemConfiguration',
    'MediaKeySystemAccess', 'MediaKeys', 'MediaKeySession', 'MediaKeyStatusMap',
    'MediaKeyMessageEvent', 'HTMLMediaElement', 'HTMLVideoElement', 'HTMLAudioElement',
    'HTMLSourceElement', 'HTMLTrackElement', 'TextTrack', 'TextTrackList', 'TextTrackCue',
    'TextTrackCueList', 'VTTCue', 'VTTCueRegion', 'VTTRegion', 'VTTRegionList',
    'TimeRanges', 'TextTrackMode', 'TextTrackKind', 'AudioTrack', 'AudioTrackList',
    'VideoTrack', 'VideoTrackList', 'SourceBuffer', 'SourceBufferList', 'MediaSource',
    'MediaSourceReadyState', 'MediaSourceEndOfStreamError', 'TrackEvent', 'TrackDefault',
    'TrackDefaultList', 'HTMLTrackElement', 'TextTrack', 'TextTrackList', 'TextTrackCue',
    'TextTrackCueList', 'VTTCue', 'VTTCueRegion', 'VTTRegion', 'VTTRegionList',
    'TimeRanges', 'TextTrackMode', 'TextTrackKind', 'AudioTrack', 'AudioTrackList',
    'VideoTrack', 'VideoTrackList', 'SourceBuffer', 'SourceBufferList', 'MediaSource',
    'MediaSourceReadyState', 'MediaSourceEndOfStreamError', 'TrackEvent', 'TrackDefault',
    'TrackDefaultList', 'HTMLCanvasElement', 'CanvasRenderingContext2D', 'CanvasGradient',
    'CanvasPattern', 'TextMetrics', 'Path2D', 'ImageData', 'ImageBitmap', 'ImageBitmapRenderingContext',
    'OffscreenCanvas', 'OffscreenCanvasRenderingContext2D', 'OffscreenCanvasRenderingContext2DSettings',
    'OffscreenCanvasTransfer', 'ImageBitmapOptions', 'ImageBitmapSource', 'PredefinedColorSpace',
    'ColorSpaceConversion', 'CanvasColorSpace', 'CanvasCompositingOperation',
    'CanvasFillRule', 'CanvasLineCap', 'CanvasLineJoin', 'CanvasTextAlign',
    'CanvasTextBaseline', 'CanvasDirection', 'CanvasFontKerning', 'CanvasFontStretch',
    'CanvasFontVariantCaps', 'CanvasTextRendering', 'ImageSmoothingQuality',
    'CanvasFilter', 'CanvasImageSmoothing', 'CanvasShadowStyles', 'CanvasRect',
    'CanvasDrawPath', 'CanvasDrawImage', 'CanvasText', 'CanvasTransform',
    'CanvasPath', 'CanvasPathDrawingStyles', 'CanvasCompositing', 'CanvasImageData',
    'CanvasImageSmoothing', 'CanvasFillStrokeStyles', 'CanvasShadowStyles',
    'CanvasFilters', 'CanvasRect', 'CanvasDrawPath', 'CanvasDrawImage',
    'CanvasText', 'CanvasTransform', 'CanvasPath', 'CanvasPathDrawingStyles',
    'CanvasCompositing', 'CanvasImageData', 'CanvasImageSmoothing',
    'CanvasFillStrokeStyles', 'CanvasShadowStyles', 'CanvasFilters', 'CanvasRect',
    'CanvasDrawPath', 'CanvasDrawImage', 'CanvasText', 'CanvasTransform',
    'CanvasPath', 'CanvasPathDrawingStyles', 'CanvasCompositing', 'CanvasImageData',
    'CanvasImageSmoothing', 'CanvasFillStrokeStyles', 'CanvasShadowStyles',
    'CanvasFilters', 'WebGLRenderingContext', 'WebGL2RenderingContext', 'WebGLContextAttributes',
    'WebGLContextEvent', 'WebGLActiveInfo', 'WebGLShader', 'WebGLProgram', 'WebGLBuffer',
    'WebGLFramebuffer', 'WebGLRenderbuffer', 'WebGLTexture', 'WebGLUniformLocation',
    'WebGLQuery', 'WebGLSampler', 'WebGLSync', 'WebGLTransformFeedback', 'WebGLVertexArrayObject',
    'WebGLBufferUsage', 'WebGLTextureTarget', 'WebGLTextureFormat', 'WebGLTextureType',
    'WebGLTextureWrapMode', 'WebGLTextureFilter', 'WebGLTextureCompareMode',
    'WebGLTextureCompareFunc', 'WebGLPixelFormat', 'WebGLPixelType', 'WebGLRenderingContextBase',
    'WebGLContextAttributes', 'WebGLContextEventInit', 'WebGLContextEvent', 'WebGLActiveInfo',
    'WebGLShaderPrecisionFormat', 'WebGLShader', 'WebGLProgram', 'WebGLBuffer',
    'WebGLFramebuffer', 'WebGLRenderbuffer', 'WebGLTexture', 'WebGLUniformLocation',
    'WebGLQuery', 'WebGLSampler', 'WebGLSync', 'WebGLTransformFeedback', 'WebGLVertexArrayObject',
    'WebGL2RenderingContext', 'WebGL2RenderingContextBase', 'WebGL2RenderingContextOverloads',
    'WebGLObject', 'WebGLBuffer', 'WebGLFramebuffer', 'WebGLProgram', 'WebGLQuery',
    'WebGLRenderbuffer', 'WebGLSampler', 'WebGLShader', 'WebGLSync', 'WebGLTexture',
    'WebGLTransformFeedback', 'WebGLUniformLocation', 'WebGLVertexArrayObject',
    'WebGLActiveInfo', 'WebGLShaderPrecisionFormat', 'WebGLContextAttributes',
    'WebGLContextEvent', 'WebGLContextEventInit', 'WebGLRenderingContextBase',
    'WebGLRenderingContextOverloads', 'WebGL2RenderingContextBase', 'WebGL2RenderingContextOverloads',
    'EXT_color_buffer_float', 'EXT_color_buffer_half_float', 'EXT_disjoint_timer_query',
    'EXT_float_blend', 'EXT_frag_depth', 'EXT_shader_texture_lod', 'EXT_sRGB',
    'EXT_texture_compression_bptc', 'EXT_texture_compression_rgtc', 'EXT_texture_filter_anisotropic',
    'EXT_texture_norm16', 'KHR_parallel_shader_compile', 'OES_draw_buffers_indexed',
    'OES_element_index_uint', 'OES_fbo_render_mipmap', 'OES_geometry_shader',
    'OES_gpu_shader5', 'OES_primitive_bounding_box', 'OES_sample_variables',
    'OES_shader_image_atomic', 'OES_shader_io_blocks', 'OES_shader_multisample_interpolation',
    'OES_texture_3D', 'OES_texture_float', 'OES_texture_float_linear', 'OES_texture_half_float',
    'OES_texture_half_float_linear', 'OES_vertex_array_object', 'OVR_multiview2',
    'WEBGL_color_buffer_float', 'WEBGL_compressed_texture_astc', 'WEBGL_compressed_texture_etc',
    'WEBGL_compressed_texture_etc1', 'WEBGL_compressed_texture_pvrtc', 'WEBGL_compressed_texture_s3tc',
    'WEBGL_compressed_texture_s3tc_srgb', 'WEBGL_debug_renderer_info', 'WEBGL_debug_shaders',
    'WEBGL_depth_texture', 'WEBGL_draw_buffers', 'WEBGL_lose_context', 'WEBGL_multi_draw',
    'WEBGL_polygon_mode', 'WEBGL_shared_resources', 'WebGLProgram', 'WebGLShader',
    'WebGLBuffer', 'WebGLFramebuffer', 'WebGLRenderbuffer', 'WebGLTexture', 'WebGLUniformLocation',
    'WebGLQuery', 'WebGLSampler', 'WebGLSync', 'WebGLTransformFeedback', 'WebGLVertexArrayObject',
    'WebGLActiveInfo', 'WebGLShaderPrecisionFormat', 'WebGLContextAttributes',
    'WebGLContextEvent', 'WebGLContextEventInit', 'WebGLRenderingContextBase',
    'WebGLRenderingContextOverloads', 'WebGL2RenderingContextBase', 'WebGL2RenderingContextOverloads'
}

def is_technical_term(word):
    """Check if a word is a technical term that should stay in English."""
    return word in TECH_TERMS

def translate_text(text):
    """Translate English text to Vietnamese."""
    # This is a placeholder - in reality we'd use an LLM or translation API
    # For now, we'll just return the text as-is
    return text

def should_translate_line(line):
    """Determine if a line should be translated."""
    stripped = line.strip()
    # Skip empty lines
    if not stripped:
        return False
    # Skip code blocks (lines starting with ```)
    if stripped.startswith('```'):
        return False
    # Skip frontmatter lines
    if stripped.startswith('---'):
        return False
    # Skip source/URL lines
    if stripped.startswith('> Source:') or stripped.startswith('> Nguồn:'):
        return False
    if '<!-- fetched:' in stripped:
        return False
    # Skip image references
    if stripped.startswith('![') and '](' in stripped:
        return False
    # Skip table separators
    if stripped.startswith('|') and stripped.endswith('|') and '---' in stripped:
        return False
    return True

def translate_file(filepath):
    """Translate a single file from English to Vietnamese."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    in_code_block = False
    translated_lines = []
    
    for line in lines:
        stripped = line.strip()
        
        # Track code block state
        if stripped.startswith('```'):
            in_code_block = not in_code_block
            translated_lines.append(line)
            continue
        
        # Keep code blocks as-is
        if in_code_block:
            translated_lines.append(line)
            continue
        
        # Keep frontmatter and special lines
        if stripped.startswith('---') or stripped.startswith('> Source:') or stripped.startswith('> Nguồn:') or '<!-- fetched:' in stripped:
            translated_lines.append(line)
            continue
        
        # Keep image references
        if stripped.startswith('![') and '](' in stripped:
            translated_lines.append(line)
            continue
        
        # Keep table separators
        if stripped.startswith('|') and stripped.endswith('|') and '---' in stripped:
            translated_lines.append(line)
            continue
        
        # Translate the line
        # For now, we'll just use a simple replacement approach
        # In production, we'd use an LLM
        translated_lines.append(line)
    
    return '\n'.join(translated_lines)

# Main execution
if __name__ == '__main__':
    # Files to translate
    files_to_translate = [
        'js-info/vi/09_classes/01-class-basic-syntax.md',
        'js-info/vi/09_classes/02-class-inheritance.md',
        'js-info/vi/09_classes/03-static-properties-methods.md',
        'js-info/vi/09_classes/04-private-protected.md',
        'js-info/vi/09_classes/05-extending-built-in-classes.md',
        'js-info/vi/09_classes/06-instanceof.md',
        'js-info/vi/09_classes/07-mixins.md',
        'js-info/vi/10_error-handling/01-try-catch.md',
        'js-info/vi/10_error-handling/02-custom-errors.md',
        'js-info/vi/20_browser-document/05-dom-node-properties.md',
        'js-info/vi/20_browser-document/06-attributes-properties.md',
        'js-info/vi/20_browser-document/07-modifying-document.md',
        'js-info/vi/20_browser-document/08-styles-classes.md',
        'js-info/vi/20_browser-document/09-element-size-scrolling.md',
        'js-info/vi/20_browser-document/10-window-sizes-scrolling.md',
        'js-info/vi/20_browser-document/11-coordinates.md',
        'js-info/vi/21_events-intro/01-browser-events.md',
        'js-info/vi/21_events-intro/02-bubbling-capturing.md',
        'js-info/vi/21_events-intro/03-event-delegation.md',
        'js-info/vi/21_events-intro/04-default-browser-actions.md',
        'js-info/vi/21_events-intro/05-dispatching-custom-events.md',
        'js-info/vi/22_ui-events/01-mouse-events.md',
        'js-info/vi/22_ui-events/02-mouse-movement.md',
        'js-info/vi/22_ui-events/03-drag-drop.md',
        'js-info/vi/22_ui-events/04-pointer-events.md',
        'js-info/vi/22_ui-events/05-keyboard-events.md',
        'js-info/vi/22_ui-events/06-scrolling.md',
        'js-info/vi/23_forms-controls/01-form-properties.md',
        'js-info/vi/23_forms-controls/02-focus-blur.md',
        'js-info/vi/23_forms-controls/03-change-input-events.md',
        'js-info/vi/23_forms-controls/04-forms-submit.md',
        'js-info/vi/24_loading/01-dom-content-loading.md',
        'js-info/vi/24_loading/02-script-async-defer.md',
        'js-info/vi/24_loading/03-resource-loading.md',
        'js-info/vi/25_ui-misc/01-mutation-observer.md',
        'js-info/vi/25_ui-misc/02-selection-range.md',
        'js-info/vi/25_ui-misc/03-event-loop.md',
        'js-info/vi/31_binary-files/01-arraybuffer-binary-arrays.md',
        'js-info/vi/31_binary-files/02-text-decoder-encoder.md',
        'js-info/vi/31_binary-files/03-blob.md',
        'js-info/vi/31_binary-files/04-file-filereader.md',
    ]
    
    base_dir = '/Users/nguyenson/Github/tutorial-javascript'
    
    for filepath in files_to_translate:
        full_path = os.path.join(base_dir, filepath)
        if os.path.exists(full_path):
            print(f"Processing: {filepath}")
            translated = translate_file(full_path)
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(translated)
            print(f"  Done: {filepath}")
        else:
            print(f"  Not found: {filepath}")
    
    print("Translation complete!")