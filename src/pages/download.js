import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import clsx from 'clsx';
import Layout from '@theme/Layout';
import Download from '@site/src/components/Download';
import styles from './download.module.css';

export default function Home() {
    
    const {siteConfig} = useDocusaurusContext();
    return (
        <Layout title="下载" description="下载页面">
        <div
          className={clsx('hero hero--primary', styles.heroBanner)}
          style={{
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'center',
            // height: '50vh',
            padding: '1vh',
            fontSize: '20px',
          }}>
          <Download/>
                  
        </div>
      </Layout>
    );
  }
  