import AvatarCanvas from "./live2d/Live2DCanvas";

export default function AvatarStage(){

    return (
        <div
            style={{
                width:"100%",
                height:"100%",
                overflow:"hidden",
                position:"relative"
            }}
        >

            <AvatarCanvas />

        </div>
    );
}