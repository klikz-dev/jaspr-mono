import axios from 'axios';
import actionNames from './actionNames';
import Sentry from 'lib/sentry';
import Segment from 'lib/segment';
import config from 'config';

interface BodyType {
    clientTimestamp: string;
    action: string;
    screen?: string;
    extra?: string;
    sectionUid?: string;
}

interface ExtraActionData {
    screen?: string;
    extra?: string;
    sectionUid?: string;
}

class InOrderAction {
    clientTimestamp: Date;
    name: string;
    screen?: string;
    extra?: string;
    sectionUid?: string;
    manager: ActionManager;
    posted: boolean;
    nextAction: InOrderAction | null;

    // Prepare the `InOrderAction` for being sent to the server.
    constructor(
        name: string,
        manager: ActionManager,
        screen?: string,
        extra?: string,
        sectionUid?: string,
    ) {
        this.clientTimestamp = new Date();
        this.name = name;
        this.screen = screen;
        this.extra = extra;
        this.sectionUid = sectionUid;
        this.posted = false;
        this.manager = manager;
        this.nextAction = null;
    }

    // Send the `InOrderAction` to the server.
    async send(): Promise<void> {
        const body: BodyType = {
            clientTimestamp: this.clientTimestamp.toISOString(),
            action: this.name,
        };
        if (this.screen) {
            body.screen = this.screen.substring(0, 63);
        }
        if (this.extra) {
            body.extra = this.extra.substring(0, 127);
        }
        if (this.sectionUid) {
            body.sectionUid = this.sectionUid;
        }
        try {
            Segment.track(this.name, body);
            await axios.post(`${config.apiRoot}/patient/action`, body);
        } catch (err) {
            console.error(err);
            Sentry.captureException(err);
        } finally {
            this.posted = true;
            if (this.nextAction) {
                this.nextAction.send();
            } else {
                // If there is no `nextAction`, we must be the latest,
                // and since we're done we can set `latest` on our
                // `ActionManager` to `null`.
                this.manager.latest = null;
            }
        }
    }
}

class ActionManager {
    latest: InOrderAction | null;
    constructor() {
        this.latest = null;
    }

    async add(actionName: string, screen?: string, extra?: string, sectionUid?: string) {
        const action = new InOrderAction(actionName, this, screen, extra, sectionUid);
        if (this.latest === null || this.latest === undefined) {
            this.latest = action;
            this.latest.send();
        } else {
            // This part of the code relies on `InOrderAction.send()` correctly
            // setting `this.latest` to `null` if there is no following action
            // (which that part of the code currently does). If this ever gets changed,
            // be careful to check that part of the code too.
            this.latest.nextAction = action;
            this.latest = action;
        }
    }
}

const actionManager = new ActionManager();

const addAction = async (actionName: string, actionData: ExtraActionData = {}) => {
    const { screen, extra, sectionUid } = actionData;
    await actionManager.add(actionName, screen, extra, sectionUid);
};

export { actionManager, addAction, actionNames };
