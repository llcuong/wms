import { useTranslation } from "react-i18next";

import type { PageNavigatorComponent } from "@routes/types";

import { EditIcon, NoUsersIcon, PlusIcon } from "@icons";

import { Base } from "./Base";
import AddUserModal from "./AddUser/Index";
import CreateAccountModal from "./AddAccount/Index";
import useManageAccount from "./useManageAccount";

const formatDate = (dateString: string | null): string => {
    if (!dateString) return "—";
    const date = new Date(dateString);
    return date.toLocaleDateString("en-US", {
        year: "numeric",
        month: "short",
        day: "numeric",
        hour: "2-digit",
        minute: "2-digit",
    });
};

const Index: PageNavigatorComponent = (props) => {
    const { t } = useTranslation();

    const {
        users,
        isLoading,
        error,
        isAddUserModalOpen,
        isAddAccountModalOpen,
        selectedUserId,

        setIsAddUserModalOpen,
        setIsAddAccountModalOpen,
        setSelectedUserId,
        getUserList,
        openCreateAccountModal,
    } = useManageAccount();

    const getStatusColor = (key: string, status: string) => {
        switch (key) {
            case 'bg':
                switch (status) {
                    case 'active': return 'bg-emerald-100 text-emerald-700';
                    case 'pending': return 'bg-yellow-100 text-yellow-700';
                    case 'deleted': return 'bg-red-100 text-red-700';
                    default: return;
                };
            case 'text':
                switch (status) {
                    case 'active': return 'bg-emerald-500';
                    case 'pending': return 'bg-yellow-500';
                    case 'deleted': return 'bg-red-500';
                    default: return;
                };
            default: return;
        };
    };

    const TH_LIST = [
        "label.userInfo", "label.email", "label.status", "label.accountId", "label.lastLogin", "label.actions",
    ];

    return (
        <Base
            currentApp={props.currentApp}
            navigateApp={props.navigateApp}
            navigatePage={props.navigatePage}
        >
            <div className="bg-(--bg-primary)) container mx-auto px-4 py-8">
                {/* Header */}
                <div className="flex items-center justify-between mb-8">
                    <div>
                        <h1 className="text-3xl font-bold bg-(--color-primary) bg-clip-text text-transparent">
                            {t("title.userManagement")}
                        </h1>
                        <p className="text-(--text-secondary) mt-1">{t("description.userManagement")}</p>
                    </div>
                    <button type="button"
                        onClick={() => setIsAddUserModalOpen(true)}
                        className="group flex items-center gap-2 px-5 py-2.5 bg-green-600 text-white rounded-xl cursor-pointer 
                                        transition-all hover:bg-green-800 hover:shadow-indigo-500/40 shadow-lg shadow-indigo-500/25"
                    >
                        <PlusIcon />
                        <span className="font-medium">{t("button.addUser")}</span>
                    </button>
                </div>

                {/* Content */}
                {isLoading ? (
                    <div className="flex items-center justify-center py-20">
                        <div className="flex flex-col items-center gap-4">
                            <div className="w-12 h-12 border-4 border-indigo-600/30 border-t-indigo-600 rounded-full animate-spin"></div>
                            <p className="text-(text-primary) font-medium">{t("status.loadingUser")}</p>
                        </div>
                    </div>
                ) : error ? (
                    <div className="bg-red-50 border border-red-200 rounded-xl p-6 text-center">
                        <div className="text-red-600 font-medium">{error}</div>
                        <button type="button"
                            onClick={getUserList}
                            className="mt-4 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-all duration-300 cursor-pointer"
                        >
                            {t("button.retry")}
                        </button>
                    </div>
                ) : (
                    <div className="bg-(--bg-primary) rounded-2xl shadow-xl shadow-gray-200/50 overflow-hidden border border-(--color-secondary)">
                        {/* Table */}
                        <div className="overflow-x-auto">
                            <table className="w-full">
                                <thead>
                                    <tr className="bg-(--bg-secondary) border-b border-(--color-secondary)">
                                        {TH_LIST.map((th, idx) => (
                                            <th key={idx} className="text-left px-6 py-4 text-xs font-semibold text-(--text-secondary) tracking-wider">
                                                {t(th)}
                                            </th>
                                        ))}
                                    </tr>
                                </thead>
                                <tbody className="divide-y divide-(--color-secondary)">
                                    {users.length === 0 ? (
                                        <tr>
                                            <td colSpan={6} className="px-6 py-16 text-center">
                                                <div className="flex flex-col items-center gap-3">
                                                    <div className="w-16 h-16 bg-(--bg-secondary) rounded-full flex items-center justify-center">
                                                        <NoUsersIcon />
                                                    </div>
                                                    <p className="text-(--text-secondary) font-medium">{t("notification.noUsers")}</p>
                                                    <p className="text-(--text-secondary) text-sm">{t("hint.noUsers")}</p>
                                                </div>
                                            </td>
                                        </tr>
                                    ) : (
                                        users.map((user) => (
                                            <tr key={user.id}>
                                                <td className="px-6 py-4">
                                                    <div className="flex items-center gap-3">
                                                        <div className="w-10 h-10 bg-(--color-primary) rounded-full flex items-center justify-center text-(--bg-secondary) font-semibold text-sm shadow-lg shadow-indigo-500/25">
                                                            {user.user_full_name.charAt(0).toUpperCase()}
                                                        </div>
                                                        <div>
                                                            <div className="font-semibold text-(--text-primary)">
                                                                {user.user_full_name}
                                                            </div>
                                                            <div className="text-sm text-(--text-primary)">
                                                                <span className="font-mono bg-(--color-secondary) px-1.5 py-0.5 rounded text-xs">
                                                                    {user.user_id}
                                                                </span>
                                                                <span className="mx-1">•</span>
                                                                <span>@{user.user_name}</span>
                                                            </div>
                                                        </div>
                                                    </div>
                                                </td>

                                                {/* Email */}
                                                <td className="px-6 py-4">
                                                    <span className="text-(--text-primary)">
                                                        {user.user_email || "—"}
                                                    </span>
                                                </td>

                                                {/* Status */}
                                                <td className="px-6 py-4">
                                                    <span className={`inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium
                                                                    ${getStatusColor("bg", user.user_status_name.toLowerCase())}`}
                                                    >
                                                        <span className={`w-1.5 h-1.5 rounded-full mr-1.5
                                                                        ${getStatusColor("text", user.user_status_name.toLowerCase())}`}
                                                        ></span>
                                                        {t(`status.${user.user_status_name}`)}
                                                    </span>
                                                </td>

                                                {/* Account ID */}
                                                <td className="px-6 py-4">
                                                    {user.has_account && user.account ? (
                                                        <span className="font-mono text-sm bg-indigo-50 text-indigo-700 px-2 py-1 rounded">
                                                            {user.account.account_id}
                                                        </span>
                                                    ) : (
                                                        <span className="text-(--text-secondary) italic">
                                                            {t("notification.noAccount")}
                                                        </span>
                                                    )}
                                                </td>

                                                {/* Last Login */}
                                                <td className="px-6 py-4">
                                                    <span className="text-sm text-(--text-primary)">
                                                        {user.account
                                                            ? formatDate(user.account.account_last_login)
                                                            : "—"}
                                                    </span>
                                                </td>

                                                <td className="px-6 py-4 text-left">
                                                    {user.has_account ? (
                                                        <button type="button"
                                                            className="inline-flex items-center gap-1.5 px-3 py-1.5 text-sm font-medium cursor-pointer
                                                                        text-indigo-600 bg-indigo-50 rounded-lg hover:bg-indigo-100 transition-colors duration-300">
                                                            <EditIcon />
                                                            {t("button.edit")}
                                                        </button>
                                                    ) : user.user_status_name.toLowerCase() !== "deleted" && (
                                                        <button type="button"
                                                            onClick={() => openCreateAccountModal(user.user_id)}
                                                            className="inline-flex items-center gap-1.5 px-3 py-1.5 text-sm font-medium cursor-pointer
                                                                        text-emerald-600 bg-emerald-50 rounded-lg hover:bg-emerald-100 transition-colors duration-300"
                                                        >
                                                            <PlusIcon />
                                                            {t("button.addAccount")}
                                                        </button>
                                                    )}
                                                </td>
                                            </tr>
                                        ))
                                    )}
                                </tbody>
                            </table>
                        </div>

                        {/* Footer */}
                        {users.length > 0 && (
                            <div className="px-6 py-4 border-t bg-(--bg-secondary) border-(--color-secondary)">
                                <p className="text-sm text-(--text-secondary)">
                                    Showing <span className="font-medium text-(--text-primary)">{users.length}</span> users
                                </p>
                            </div>
                        )}
                    </div>
                )}
            </div>

            <AddUserModal
                isOpen={isAddUserModalOpen} setIsOpen={setIsAddUserModalOpen}
                getUserList={getUserList}
            />
            <CreateAccountModal
                isOpen={isAddAccountModalOpen} setIsOpen={setIsAddAccountModalOpen}
                userId={selectedUserId} setUserId={setSelectedUserId}
                getUserList={getUserList}
            />
        </Base>
    );
};

export default Index;