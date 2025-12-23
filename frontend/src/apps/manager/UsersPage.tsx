import { Base } from "./Base";
import type { PageNavigatorComponent } from "@routes/types";
import { UserManager } from "@modules/AccountManager";

const UsersPage: PageNavigatorComponent = (props) => {
    return (
        <Base
            currentApp={props.currentApp}
            navigateApp={props.navigateApp}
            navigatePage={props.navigatePage}>
            <div className="container mx-auto">
                <div className="mb-4">
                    <button
                        onClick={() => props.navigatePage('index')}
                        className="flex items-center gap-2 text-gray-600 hover:text-gray-900 transition-colors"
                    >
                        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
                        </svg>
                        Back to Dashboard
                    </button>
                </div>
                <UserManager />
            </div>
        </Base>
    );
};

export default UsersPage;
