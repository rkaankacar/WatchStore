import React from 'react';

export default function FAQ() {
  const faqs = [
    {
      id: 1,
      question: "Ürünleriniz orijinal mi?",
      answer: "Evet, WatchStore'da satılan tüm saatler %100 orijinal ve faturalıdır.",
    },
    {
      id: 2,
      question: "Kargo ne kadar sürede gelir?",
      answer: "Siparişler genellikle 1–3 iş günü içinde kargoya teslim edilir.",
    },
    {
      id: 3,
      question: "İade veya değişim yapabilir miyim?",
      answer: "Ürünü teslim aldıktan sonra 14 gün içinde iade veya değişim talep edebilirsiniz.",
    },
    {
      id: 4,
      question: "Saatlerin garanti süresi nedir?",
      answer: "Tüm ürünler, marka tarafından sağlanan resmi garanti kapsamında gönderilir (genellikle 2 yıl).",
    },
    {
      id: 5,
      question: "Ödeme yöntemleriniz neler?",
      answer: "Kredi kartı, banka kartı ve iyzico güvenli ödeme altyapısı ile ödeme yapabilirsiniz.",
    },
    {
      id: 6,
      question: "Kargoyu teslim alırken neye dikkat etmeliyim?",
      answer: "Paketinizi teslim almadan önce hasar kontrolü yapmanız önerilir. Hasar varsa kargo tutanağı tutturmanız yeterlidir.",
    },
    {
      id: 7,
      question: "Siparişimi nasıl takip ederim?",
      answer: "Siparişiniz kargoya verildiğinde SMS veya e-posta ile takip numarası gönderilir.",
    },
    {
      id: 8,
      question: "Fatura nasıl gönderiliyor?",
      answer: "Tüm siparişlerin faturası dijital olarak e-posta adresinize gönderilir.",
    },
  ];

  return (
    <div className="container my-5" style={{ minHeight: '60vh' }}>
      <h2 className="text-center mb-5">❓ Sıkça Sorulan Sorular (S.S.S)</h2>

      {faqs.map((faq) => (
        <div key={faq.id} className="card mb-3 shadow-sm">
          <div className="card-header bg-dark">
            <h5 className="mb-0 text-warning">
              {faq.question}
            </h5>
          </div>
          <div className="card-body">
            <p className="card-text">{faq.answer}</p>
          </div>
        </div>
      ))}
    </div>
  );
}
