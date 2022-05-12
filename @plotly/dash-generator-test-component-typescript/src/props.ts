// Needs to export types if not in a d.ts file or if any import is present in the d.ts
import React from 'react';

export type TypescriptComponentProps = {
    children?: React.ReactNode;
    id?: string;
    /**
     * A string
     */
    required_string: string;
    a_string?: string;
    a_number?: number;
    a_bool?: boolean;
    obj?: {
        value: any;
        label?: string;
    };
    array_string?: string[];
    array_number?: number[];
    array_obj?: {a: string}[];
    array_any?: any[];
    enum_string?: 'one' | 'two';
    union?: number | string;
    union_shape?: {a: string} | string;
    array_union_shape?: ({a: string} | string)[];
    element?: JSX.Element;
    array_elements?: JSX.Element[];

    string_default?: string;
    number_default?: string;
    obj_default?: {a: string; b: number};
    bool_default?: boolean;
    null_default?: any;

    setProps?: (props: Record<string, any>) => void;
    className?: string;
    style?: any;
};
