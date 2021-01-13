import React, { useEffect } from 'react';

const Comp = () => {

    useEffect(() => {
        fetch('dist_list').then(res => res.json()).then(data => {
            console.log(data);
        });

        fetch('generate?loc=1&scale=1&dist=norm&function=pdf').then(res => res.json()).then(data => {
            console.log(data);
        });
    }, [])

    return (
        <div className="comp">comp contents</div>
    )
}

export default Comp;