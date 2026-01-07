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
                    <p>Welcome to Former Warehouse</p>
                </div>
                <button onClick={() => props.navigatePage('add-basket')} className="mt-4 bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600">
                    Add Basket
                </button>
            </div>
        </Base>
    );
};

export default Index;