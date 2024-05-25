import React from "react";

const HomePage = () => {
    return (
        <>
            <div className="text-3xl font-bold pt-10">Welcome</div>
            <p className="text-xl mt-5">
                In this tutorial you will learn how to use:
            </p>
            <ol className="ml-8 mt-5 list-decimal">
                <li>react-bootstrap</li>
                <li>react-hook-form with yup validation</li>
                <li>CRUD functionality - Create Read Update Delete</li>
                <li>file upload with NestJS</li>
                <li>connect ReactJS and NestJS</li>
                <li>setup NestJS with custom logging</li>
                <li>connect to PostgreSQL database using TypeORM</li>
                <li>create dtos with validation</li>
                <li>deploy ReactJS to AWS S3 Bucket</li>
                <li>deploy NestJS to AWS ECS (Elastic Container Service)</li>
            </ol>
        </>
    );
};

export default HomePage;
