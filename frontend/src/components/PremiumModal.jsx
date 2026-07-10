import "./PremiumModal.css";

export default function PremiumModal({

    open,
    onClose,
    user,
    onUpgrade

}){

    if(!open) return null;

    return(

        <div className="premium-overlay">

            <div className="premium-box">

                <button
                    className="premium-close"
                    onClick={onClose}
                >
                    ✕
                </button>

                <h2>⭐ Premium Beta</h2>

                <p className="premium-desc">
                    Unlock all AI Companion features.
                </p>

                <div className="premium-card">

                    <h3>Premium 7 Hari</h3>

                    <div className="premium-price">

                        Rp 9.000

                    </div>

                    <ul>

                        <li>✔ Unlimited Chat</li>

                        <li>✔ Premium Voice</li>

                        <li>✔ Early Access</li>

                    </ul>

                    {
                        user?.plan==="PREMIUM"

                        ?

                        <button
                            className="premium-active"
                            disabled
                        >
                            Premium Active
                        </button>

                        :

                        <button
                            className="premium-upgrade"
                            onClick={onUpgrade}
                        >
                            Upgrade
                        </button>

                    }

                </div>

                <div className="coming-card">

                    <h3>

                        Premium Bulanan

                    </h3>

                    <span>

                        Coming Soon

                    </span>

                </div>

            </div>

        </div>

    );

}