import { LAppDelegate } from "./lappdelegate";

export class CubismApp {

    static start() {

        if (!LAppDelegate.getInstance().initialize()) {

            console.error("Live2D initialize failed.");

            return;

        }

        LAppDelegate.getInstance().run();

    }

    static dispose() {

        LAppDelegate.releaseInstance();

    }

}