import { Locale } from "@/components/intl";

export const DONATION_CONFIG: Record<Locale, { buyButtonId: string; publishableKey: string }> = {
  en: {
    buyButtonId: "buy_btn_1SA6zyASmawTdJcy077G1ZOj",
    publishableKey: "pk_live_51S9B6GASmawTdJcyQ1lrfyFvuGfciQ7Kci0Sw11AGBGjg7dbH0KlbFUOjpcD96LtyWT3JGhpS4oWfIjtHAoCFbo500O7bzQ4Nr",
  },
  pl: {
    buyButtonId: "buy_btn_1SA6NzASmawTdJcyyd6YboOh",
    publishableKey: "pk_live_51S9B6GASmawTdJcyQ1lrfyFvuGfciQ7Kci0Sw11AGBGjg7dbH0KlbFUOjpcD96LtyWT3JGhpS4oWfIjtHAoCFbo500O7bzQ4Nr",
  },
};

export function DonationWidget({ lang, className }: { lang: Locale; className?: string }) {
  const donationConfig = DONATION_CONFIG[lang];

  if (!donationConfig) {
    return null;
  }

  const wrapperClass = className ?? "";
  const wrapperStyle = className ? undefined : { display: "flex", marginTop: "1rem" };

  return (
    <div className={wrapperClass} style={wrapperStyle}>
      {/* @ts-expect-error: custom element provided by Stripe */}
      <stripe-buy-button
        buy-button-id={donationConfig.buyButtonId}
        publishable-key={donationConfig.publishableKey}
      />
    </div>
  );
}
