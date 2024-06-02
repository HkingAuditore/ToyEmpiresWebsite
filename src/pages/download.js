import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import Download from '@site/src/components/Download';

export default function Home() {
    
    const {siteConfig} = useDocusaurusContext();
    return (
        <Layout title="Hello" description="Hello React Page">
        <div
          style={{
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'center',
            height: '50vh',
            fontSize: '20px',
          }}>
          <Download/>
                  
        </div>
      </Layout>
    );
  }
  