import { Base } from "./Base";
import type { PageNavigatorComponent } from "@routes/types";

const Index: PageNavigatorComponent = (props) => {
    return (
        <Base
            currentApp={props.currentApp}
            navigateApp={props.navigateApp}
            navigatePage={props.navigatePage}>
            <div className="container mx-auto">
                <h1 className="text-2xl font-bold mb-4">Administration Dashboard</h1>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {/* Users Card */}
                    <div
                        onClick={() => props.navigatePage('users')}
                        className="bg-gradient-to-br from-indigo-500 to-purple-600 p-6 rounded-xl shadow-lg cursor-pointer hover:shadow-xl transition-all hover:scale-105"
                    >
                        <div className="flex items-center gap-4">
                            <div className="w-12 h-12 bg-white/20 rounded-lg flex items-center justify-center">
                                <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5-9a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0z" />
                                </svg>
                            </div>
                            <div>
                                <h3 className="text-lg font-semibold text-white">User Management</h3>
                                <p className="text-indigo-100 text-sm">Manage system users</p>
                            </div>
                        </div>
                    </div>

                    {/* Accounts Card */}
                    <div
                        onClick={() => props.navigatePage('accounts')}
                        className="bg-gradient-to-br from-emerald-500 to-teal-600 p-6 rounded-xl shadow-lg cursor-pointer hover:shadow-xl transition-all hover:scale-105"
                    >
                        <div className="flex items-center gap-4">
                            <div className="w-12 h-12 bg-white/20 rounded-lg flex items-center justify-center">
                                <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z" />
                                </svg>
                            </div>
                            <div>
                                <h3 className="text-lg font-semibold text-white">Account Management</h3>
                                <p className="text-emerald-100 text-sm">Manage login accounts</p>
                            </div>
                        </div>
                    </div>

                    {/* Settings Card */}
                    <div className="bg-gradient-to-br from-gray-500 to-slate-600 p-6 rounded-xl shadow-lg cursor-pointer hover:shadow-xl transition-all hover:scale-105">
                        <div className="flex items-center gap-4">
                            <div className="w-12 h-12 bg-white/20 rounded-lg flex items-center justify-center">
                                <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                                </svg>
                            </div>
                            <div>
                                <h3 className="text-lg font-semibold text-white">System Settings</h3>
                                <p className="text-gray-200 text-sm">Coming soon...</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </Base>
    );
};

export default Index;
