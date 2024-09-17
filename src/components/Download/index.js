
import styles from './styles.module.css';
import React, { useState } from 'react';
import { NextUIProvider } from "@nextui-org/react";
import { Image, Button } from "@nextui-org/react";
import { FaGamepad } from "react-icons/fa";
import { FaAndroid } from "react-icons/fa";
import { FaWindows } from "react-icons/fa";
import { FaSteam } from "react-icons/fa";
import { Chip, Avatar } from "@nextui-org/react";
import { Link } from 'react-router-dom';
import clsx from 'clsx';


export default function Download() {

    return (
        <NextUIProvider>


            <div class="grid grid-cols-2 gap-4">
                <div class="col-span-2 w-full place-items-center self-center"
                    >
                    <Image
                        isBlurred
                        shadow='lg'
                        removeWrapper
                        src={require('@site/static/img/icon.png').default}
                        className={clsx('imgIcon', styles.imgIcon)}
                    />
                </div>
                <div class="col-span-2">
                    <h1>现在下载</h1>
                    <Chip
                        variant="flat"
                        avatar={
                            <Avatar name="V" size="sm" getInitials={(name) => name.charAt(0)} />
                        }
                    >
                        0.181.2.10
                    </Chip>
                </div>
                <div>
                    <a href='/download/ToyEmpires_Android_0.181.2.10.apk'>
                    <Button  fullWidth="true" color="success" className="bg-gradient-to-tr from-green-500 to-yellow-500 text-white shadow-lg" radius="full" variant="shadow" startContent={<FaAndroid />}>
                        <b>Android</b> 安装包下载
                    </Button>
                    </a>

                </div>
                <div>
                    <a href="https://l.taptap.cn/gsHfzapN?channel=rep-rep_kgfqorsukvm" target="_blank">
                    <Button fullWidth="true" color="success" radius="full" className="bg-gradient-to-tr from-green-500 to-yellow-500 text-white shadow-lg" variant="shadow" startContent={<FaGamepad />}>
                        前往<b><i>Taptap</i></b>下载
                    </Button>
                    </a>

                </div>

                <div>
                <a href='/download/ToyEmpires_Win_0.181.2.10.exe'>
                    <Button fullWidth="true" color="primary" className="bg-gradient-to-tr from-green-500 to-blue-500 text-white shadow-lg" radius="full" variant="shadow" startContent={<FaWindows />}>
                        <b>Windows</b> 安装包下载
                    </Button>
                    </a>
                </div>
                <div>
                    <a href="https://store.steampowered.com/app/2773270" target="_blank">
                    <Button fullWidth="true" color="primary" radius="full" className="bg-gradient-to-tr from-green-500 to-blue-500 text-white shadow-lg" variant="shadow" startContent={<FaSteam />}>
                        前往<b><i>Steam</i></b>下载
                    </Button>
                    </a>

                </div>
            </div>




        </NextUIProvider>

    );
}