import React, {useContext, useEffect} from 'react';
import {LibrariesContext} from './librariesContext';
import Registry from '../registry';
import {CheckedComponent} from '../CheckedComponent.react';
import {createLibraryElement} from './createLibraryElement';

type LibraryComponentProps = {
    type: string;
    namespace: string;
    props: any;
    extraProps: any;
    children: any;
    props_check: boolean;
};

const LibraryComponent = (props: LibraryComponentProps) => {
    const {props_check, namespace, type, ...rest} = props;

    const context = useContext(LibrariesContext);

    useEffect(() => {
        context.addToLoad(namespace);
    }, []);

    if (!context.isLoaded(namespace)) {
        return <></>;
    }
    const element = Registry.resolve({namespace, type});
    if (props_check) {
        return (
            <CheckedComponent
                children={rest.children}
                element={element}
                props={rest.props}
                extraProps={rest.extraProps}
                type={type}
            />
        );
    }
    return createLibraryElement(
        element,
        rest.props,
        rest.extraProps,
        rest.children
    );
};
export default LibraryComponent;
