export const createIsInSet = <T extends string | number>(ids: readonly T[]): ((value: unknown) => value is T) => {
    const set = new Set(ids);

    return (value: unknown): value is T => {
        const type = typeof value;
        return (type === "string" || type === "number") && set.has(value as T);
    };
};