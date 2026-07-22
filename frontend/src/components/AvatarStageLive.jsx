import Live2DCanvasLive2 from "./live2d/Live2dCanvasLive2";

export default function AvatarStageLive() {
    return (
        <div
            style={{
                width: "100%",
                height: "100%",
                position: "relative",
                overflow: "hidden"
            }}
        >
            <Live2DCanvasLive2 />
        </div>
    );
}