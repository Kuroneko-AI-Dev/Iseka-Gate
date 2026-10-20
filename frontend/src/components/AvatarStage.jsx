
import AvatarCanvas from "./live2d/Live2DCanvas";
import { useEffect } from "react";

export default function AvatarStage({
    avatarScale,
    setAvatarScale
}) {

   useEffect(() => {
        if (window.live2dView) {
            window.live2dView.setAvatarScale(avatarScale);
        }
    }, [avatarScale]);

   

    return (
        <div
            style={{
                width: "100%",
                height: "100%",
                overflow: "hidden",
                position: "relative"
            }}
        >
           <AvatarCanvas
    avatarScale={avatarScale}
            />
        </div>
    );
}
