import { useEffect, useRef } from "react";
import { LAppDelegate } from "../../live2d/app/lappdelegate";

export default function Live2DCanvas() {
    const canvasRef = useRef(null);

    useEffect(() => {
        console.log("CANVAS START");

        const canvas = canvasRef.current;

        if (!canvas) {
            console.log("CANVAS BELUM ADA");
            return;
        }

        const delegate = LAppDelegate.getInstance();

        // =====================================================
        // LIVE2D INITIALIZE
        // =====================================================

        try {
            delegate.initialize();
        } catch (error) {
            console.log(
                "LIVE2D INITIALIZE ERROR:",
                error
            );
        }

        // =====================================================
        // RUN HANYA SEKALI
        // =====================================================

        if (!window.__live2dRunning) {
            console.log(
                "LIVE2D START RENDER LOOP"
            );

            delegate.run();

            window.__live2dRunning = true;
        } else {
            console.log(
                "LIVE2D SUDAH RUNNING - SKIP RUN"
            );
        }

        // =====================================================
        // POINTER
        // =====================================================

        const handlePointerDown = (e) => {
            delegate.onPointerDown?.(
                e.clientX,
                e.clientY
            );
        };

        const handlePointerMove = (e) => {
            delegate.onPointerMove?.(
                e.clientX,
                e.clientY
            );
        };

        const handlePointerUp = (e) => {
            delegate.onPointerUp?.(
                e.clientX,
                e.clientY
            );
        };

        canvas.addEventListener(
            "pointerdown",
            handlePointerDown
        );

        canvas.addEventListener(
            "pointermove",
            handlePointerMove
        );

        canvas.addEventListener(
            "pointerup",
            handlePointerUp
        );

        canvas.addEventListener(
            "pointerleave",
            handlePointerUp
        );

        // =====================================================
        // SUBDELEGATE
        // =====================================================

        const subdelegate =
            delegate.getSubdelegate();

        if (!subdelegate) {
            console.log(
                "LIVE2D SUBDELEGATE BELUM ADA"
            );

            return;
        }

        const view = subdelegate.getView();

window.live2dView = view;

console.log("LIVE2D VIEW GLOBAL =", view);

        // =====================================================
        // LIVE2D MODEL
        // =====================================================

        try {
            const manager =
                subdelegate.getLive2DManager();

            const model =
                manager.getModel();

            window.live2dModel = model;

            console.log(
                "MODEL GLOBAL =",
                model
            );
        } catch (error) {
            console.log(
                "LIVE2D MODEL ERROR:",
                error
            );
        }

        // =====================================================
        // RESIZE
        // =====================================================

        const container =
            canvas.parentElement;

        let resizeTimer = null;

        const resizeLive2D = () => {
            if (!container) return;

            const rect =
                container.getBoundingClientRect();

            const width =
                Math.max(
                    1,
                    Math.floor(rect.width)
                );

            const height =
                Math.max(
                    1,
                    Math.floor(rect.height)
                );

            // CSS SIZE
            canvas.style.width =
                `${width}px`;

            canvas.style.height =
                `${height}px`;

            // DRAWING BUFFER
            const dpr =
                Math.min(
                    window.devicePixelRatio || 1,
                    2
                );

            const newWidth =
                Math.floor(width * dpr);

            const newHeight =
                Math.floor(height * dpr);

            if (
                canvas.width !== newWidth ||
                canvas.height !== newHeight
            ) {
                canvas.width =
                    newWidth;

                canvas.height =
                    newHeight;
            }

            console.log(
                "LIVE2D RESIZE:",
                width,
                "x",
                height,
                "DPR:",
                dpr
            );
        };

        // =====================================================
        // RESIZE OBSERVER
        // =====================================================

        const resizeObserver =
            new ResizeObserver(() => {

                clearTimeout(
                    resizeTimer
                );

                resizeTimer =
                    setTimeout(
                        resizeLive2D,
                        100
                    );
            });

        resizeObserver.observe(
            container
        );

        // INITIAL RESIZE
        resizeLive2D();

        // =====================================================
        // CLEANUP
        // =====================================================

        return () => {

            clearTimeout(
                resizeTimer
            );

            resizeObserver.disconnect();

            canvas.removeEventListener(
                "pointerdown",
                handlePointerDown
            );

            canvas.removeEventListener(
                "pointermove",
                handlePointerMove
            );

            canvas.removeEventListener(
                "pointerup",
                handlePointerUp
            );

            canvas.removeEventListener(
                "pointerleave",
                handlePointerUp
            );

            console.log(
                "LIVE2D CANVAS CLEANUP"
            );
        };

    }, []);

    return (
        <div className="live2d-container">

            <img
                src="/bg/room.jpg"
                alt="background"
                className="live2d-background"
            />

            <canvas
                id="live2d"
                ref={canvasRef}
                className="live2d-canvas"
            />

        </div>
    );
}