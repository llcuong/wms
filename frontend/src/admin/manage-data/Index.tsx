import type { PageNavigatorComponent } from "@routes/types";

import { Base } from "./Base";

const Index: PageNavigatorComponent = (props) => {
    return (
        <Base
            currentApp={props.currentApp}
            navigateApp={props.navigateApp}
            navigatePage={props.navigatePage}
        >
            <div className="bg-(--bg-primary)) container mx-auto px-4 py-8">
                <h1 className="text-2xl font-bold mb-4">Dashboard</h1>
                <div className="bg-white p-6 rounded-lg shadow">
                    <p>Welcome to Admin</p>
                </div>
            </div>
        </Base>
    );
};

export default Index;