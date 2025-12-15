import { Base } from "./Base";
import type { PageNavigatorComponent } from "@routes/types";

const Index: PageNavigatorComponent = (props) => {
    return (
        <Base
            currentApp={props.currentApp}
            navigateApp={props.navigateApp}
            navigatePage={props.navigatePage}>
            <div className="container mx-auto">
                <h1 className="text-2xl font-bold mb-4">Dashboard</h1>
                <div className="bg-white p-6 rounded-lg shadow">
                    <p>Welcome to ABCSDASG</p>
                </div>
            </div>
        </Base>
    );
};

export default Index;